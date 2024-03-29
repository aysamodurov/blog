
import os
os.environ['DATABASE_URL'] = 'sqlite://'

import unittest
from app import app, db
from app.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))
    
    def test_follow(self):
        u1 = User(username='alex', email='alex@mail.ru')
        u1.set_password('111')
        u2 = User(username='zender', email='zender@mail.ru')
        u2.set_password('fsg')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.follower.all(), [])
        self.assertEqual(u2.followed.all(), [])
        self.assertEqual(u2.follower.all(), [])

        u2.follow(u1)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.follower.count(), 1)
        self.assertEqual(u1.follower.first().username, 'zender')
        self.assertTrue(u2.is_following(u1))
        self.assertEqual(u2.follower.all(), [])
        self.assertEqual(u2.followed.first().username, 'alex')

        u2.unfollow(u1)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.follower.all(), [])
        self.assertFalse(u2.is_following(u1))
        self.assertEqual(u2.follower.all(), [])

    def test_followed_post(self):
        u1 = User(username='alex', email='alex@mail.ru')
        u1.set_password('111')
        u2 = User(username='zender', email='zender@mail.ru')
        u2.set_password('fsg')
        
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        
        u2.follow(u1)
        
        post1 = Post(title='Title post user1', body='First post user 1')
        u1.posts.append(post1)
        
        post2 = Post(title='Title post user2', body='First post user 2')
        u1.posts.append(post2)

        db.session.commit()
        self.assertListEqual([post2,post1], u2.followed_posts().all())
        
        u2.unfollow(u1)
        self.assertEqual(u2.followed_posts().all(), [])

if __name__ == '__main__':
    unittest.main(verbosity=2)