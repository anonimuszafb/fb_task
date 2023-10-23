from faker import Faker

fake = Faker()


def generate_random_message():
    return fake.text()