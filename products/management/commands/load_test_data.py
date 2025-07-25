import json
from django.core.management.base import BaseCommand
from products.models import Category, Product
from django.db import transaction
import requests
from django.core.files.base import ContentFile

class Command(BaseCommand):
    help = 'JSON fayllardan kategoriya va mahsulotlarni yuklaydi'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING(
            'DIQQAT! Bu buyruq barcha mavjud mahsulotlar va kategoriyalarni o\'chirib tashlaydi.'
        ))
        confirmation = input('Davom etish uchun "yes" deb yozing: ')

        if confirmation.lower() != 'yes':
            self.stdout.write(self.style.ERROR('Amal bekor qilindi.'))
            return

        self.stdout.write('Eski ma\'lumotlar o\'chirilmoqda...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Eski ma\'lumotlar muvaffaqiyatli o\'chirildi.'))

        try:
            with open('data/categories.json', 'r', encoding='utf-8') as f:
                categories_data = json.load(f)
            with open('data/products.json', 'r', encoding='utf-8') as f:
                products_data = json.load(f)
        except FileNotFoundError as e:
            self.stdout.write(self.style.ERROR(f'Fayl topilmadi: {e.filename}'))
            return

        self.stdout.write('Kategoriyalar yuklanmoqda...')
        self.json_id_to_new_instance = {}
        self._create_category_tree(categories_data, None)
        self.stdout.write(self.style.SUCCESS(f'{len(self.json_id_to_new_instance)} ta kategoriya muvaffaqiyatli yuklandi.'))

        self.stdout.write('Mahsulotlar yuklanmoqda...')
        product_count = 0
        for prod_data in products_data:
            original_category_id = prod_data.pop('category')
            category_instance = self.json_id_to_new_instance.get(original_category_id)
            image_url = prod_data.pop('image', None)

            if category_instance:
                # `create` metodi avtomatik `save()` ni chaqiradi, bu esa noyob slug yaratadi
                product = Product.objects.create(category=category_instance, **prod_data)
                
                # Agar rasm URL'i mavjud bo'lsa, uni yuklab olib saqlaymiz
                if image_url:
                    try:
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            # Fayl nomini URL'dan olamiz
                            file_name = image_url.split('/')[-1]
                            # Faylni saqlaymiz
                            product.image.save(file_name, ContentFile(response.content), save=True)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"'{product.name}' uchun rasm yuklashda xatolik: {e}"))
                
                product_count += 1
            else:
                self.stdout.write(self.style.WARNING(f"Mahsulot '{prod_data['name']}' uchun kategoriya IDsi '{original_category_id}' topilmadi. O'tkazib yuborildi."))
        
        self.stdout.write(self.style.SUCCESS(f'{product_count} ta mahsulot muvaffaqiyatli yuklandi.'))
        self.stdout.write(self.style.SUCCESS('Barcha test ma\'lumotlari muvaffaqiyatli yuklandi!'))

    def _create_category_tree(self, categories_data, parent_instance, parent_json_id=None):
        children_data = [cat for cat in categories_data if cat.get('parent') == parent_json_id]
        for child_data in children_data:
            original_id = child_data['id']
            image_url = child_data.pop('image', None) # image ni vaqtincha olib turamiz
            
            child_instance = Category.objects.create(
                name=child_data['name'],
                parent=parent_instance
            )
            
            # Agar rasm URL'i mavjud bo'lsa, uni yuklab olib saqlaymiz
            if image_url:
                try:
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        file_name = image_url.split('/')[-1]
                        child_instance.image.save(file_name, ContentFile(response.content), save=True)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"'{child_instance.name}' kategoriyasi uchun rasm yuklashda xatolik: {e}"))
            
            self.json_id_to_new_instance[original_id] = child_instance
            self._create_category_tree(categories_data, child_instance, original_id)