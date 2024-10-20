from faker import Faker
import faker_commerce

fake = Faker()
fake.add_provider(faker_commerce.Provider)

def get_products(num_products):
    products = []
    for _ in range(num_products):
        product = (
            fake.unique.ean13(),
            fake.ecommerce_name(),
            fake.sentence(),
            round(fake.random.uniform(10, 1000), 2),
            fake.ecommerce_category(),
            fake.ecommerce_price(False),
            fake.date_this_year(),
            fake.company(),
            fake.company_email(),
            fake.country_code(representation="alpha-2")
        )
        products.append(product)
        print(product)
    return products