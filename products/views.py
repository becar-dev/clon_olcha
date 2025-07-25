from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Category, Product
from .serializers import CategoryDetailSerializer, ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import ProductFilter
from rest_framework.response import Response


 # Serializerlarni yangilaymiz

class CategoryViewSet(viewsets.ModelViewSet):
    """
    Kategoriyalar uchun ViewSet. `list` va `retrieve` metodlari optimallashtirilgan.
    """
    queryset = Category.objects.all()
    # `retrieve` (detal) va boshqa amallar uchun shu serializer ishlatiladi
    serializer_class = CategoryDetailSerializer

    def list(self, request, *args, **kwargs):
        # 1. Bitta so'rov bilan BARCHA kategoriyalarni olamiz
        all_categories = Category.objects.all()
        
        # 2. Tezkor qidirish uchun xarita (dictionary) yaratamiz
        node_map = {
            cat.id: {
                'id': cat.id, 
                'name': cat.name, 
                'parent': cat.parent_id, 
                'children': []
            } for cat in all_categories
        }
        
        # 3. Daraxtni xotirada (in-memory) qurib chiqamiz
        root_nodes = []
        for cat_id, cat_node in node_map.items():
            parent_id = cat_node['parent']
            if parent_id:
                # Bolani o'z otasining 'children' ro'yxatiga qo'shamiz
                if parent_id in node_map:
                    node_map[parent_id]['children'].append(cat_node)
            else:
                # Otasi yo'q bo'lsa, demak bu asosiy (root) kategoriya
                root_nodes.append(cat_node)
                
        # 4. Tayyor natijani hech qanday qo'shimcha so'rovsiz qaytaramiz
        return Response(root_nodes)

    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        # Bu metod bitta kategoriya va uning barcha sub-kategoriyalarini
        # optimallashtirilgan holda qaytaradi.
        
        # 1. Asosiy (so'ralgan) kategoriyani olamiz
        root_category = self.get_object()
        
        # 2. Bitta so'rov bilan uning barcha avlodlarini olamiz
        all_nodes_qs = root_category.get_descendants(include_self=True)
        
        # 3. Daraxtni xotirada qurish uchun xarita (dictionary) yaratamiz
        node_map = {
            cat.id: {
                'id': cat.id, 
                'name': cat.name, 
                'slug': cat.slug,
                'image': request.build_absolute_uri(cat.image.url) if cat.image else None,
                'parent': cat.parent_id, 
                'children': []
            } for cat in all_nodes_qs
        }
        
        # 4. Daraxtni xotirada (in-memory) qurib chiqamiz
        root_node_dict = None
        for cat_id, cat_node in node_map.items():
            parent_id = cat_node['parent']
            # Agar ota-kategoriya shu daraxt ichida bo'lsa, bolani unga qo'shamiz
            if parent_id and parent_id in node_map:
                node_map[parent_id]['children'].append(cat_node)
            # Asosiy (so'ralgan) kategoriyani topib olamiz
            elif cat_id == root_category.id:
                root_node_dict = cat_node
                
        return Response(root_node_dict)



class ProductViewSet(viewsets.ModelViewSet):
    # `select_related` yordamida har bir mahsulot bilan uning kategoriyasini
    # bitta JOIN so'rovi orqali birga olamiz. Bu N+1 muammosini hal qiladi.
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

    # ViewSet uchun qaysi filter backend'larini ishlatishni ko'rsatamiz
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_class = ProductFilter

    # SearchFilter uchun sozlamalar
    search_fields = ['name', 'description'] # Nomi va tavsifi bo'yicha qidiruv (masalan, ?search=iphone)
    
    # OrderingFilter uchun sozlamalar
    ordering_fields = ['price', 'created_at'] # Narxi va yaratilgan sanasi bo'yicha saralash (masalan, ?ordering=-price)

        # Keshlashtirishni qo'shamiz:
    # `cache_page(60 * 5)` - bu natijani 5 daqiqaga (300 sekund) keshlaydi.
    # `dispatch` metodi ViewSet'ga kiruvchi barcha so'rovlarni boshqaradi,
    # shuning uchun keshni shu metodga qo'llaymiz.
    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    lookup_field = 'slug'