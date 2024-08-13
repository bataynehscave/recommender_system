from faker import Faker

def get_fake_profile(count = 10):
    fake = Faker()
    user_data = []
    for _ in range(count):
        profile = fake.profile()
        data = {
            'username': profile.get('username'),
            'password': 'password',
            'email': profile.get('email'),
            'is_active': True
        }
        if 'name' in profile:
            fname, lname = profile.get('name').split()[:2]
            data['first_name'] = ''.join(fname)
            data['last_name'] = ''.join(lname)
        user_data.append(data)
    
    return user_data

