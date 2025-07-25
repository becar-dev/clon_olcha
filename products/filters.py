import django_filters
from .models import Category, Product

def get_all_descendant_ids(category):
    """
    Berilgan kategoriya va uning barcha avlodlari (sub-kategoriyalari)
    ID'larini yagona ro'yxat qilib qaytaradi.
    """
    # Boshlang'ich ro'yxatga ota-kategoriyaning o'zini qo'shamiz
    descendant_ids = {category.id}
    # Tekshirish uchun navbatga qo'yamiz
    queue = [category]

    while queue:
        # Navbatdan bitta kategoriyani olamiz
        current_category = queue.pop(0)
        # Uning barcha "bolalarini" topamiz
        children = current_category.children.all()
        for child in children:
            # Har bir bolaning ID'sini umumiy ro'yxatga qo'shamiz
            descendant_ids.add(child.id)
            # Va uni ham kelajakda tekshirish uchun navbatga qo'yamiz
            queue.append(child)
            
    return list(descendant_ids)




class ProductFilter(django_filters.FilterSet):
    # Kategoriya bo'yicha filtrlash uchun maxsus metodni belgilaymiz
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        method='filter_by_category_with_descendants',
        label="Kategoriya (barcha sub-kategoriyalar bilan)"
    )

    class Meta:
        model = Product
        # Narx bo'yicha filtrlashni saqlab qolamiz
        fields = {
            'price': ['gte', 'lte'],
        }

    def filter_by_category_with_descendants(self, queryset, name, value):
        """
        'category' parametri kelganda ishlaydigan maxsus metod.
        'value' - bu tanlangan kategoriya obyekti.
        get_descendants(include_self=True) bitta so'rov bilan barcha avlodlarni oladi.
        """
        # Tanlangan kategoriya va uning barcha avlodlarini bitta so'rovda olamiz
        descendants = value.get_descendants(include_self=True)
        # Mahsulotlarni shu kategoriyalar ro'yxati bo'yicha samarali filtrlaymiz
        return queryset.filter(category__in=descendants)