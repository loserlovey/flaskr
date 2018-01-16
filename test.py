import sys
from flaskrapp import db
from flaskrapp.models import User, Post

def init_db():
    admin_user = User('default', username='admin',email='admin@163.com',is_admin=True)
    test_user1 = User('123',username='csy',email='csy@163.com',is_admin=False)
    test_user2 = User('123',username='csy2',email='csy2@163.com',is_admin=False)
    test_user3 = User('123',username='csy3',email='csy3@163.com',is_admin=False)
    test_user4 = User('123',username='csy4',email='csy4@163.com',is_admin=False)

    post1 = Post(title='Blog1',body='Beautiful is better than ugly.',author=test_user1)
    post2 = Post(title='Blog2',body='Explicit is better than implicit.',author=test_user1)
    post3 = Post(title='Blog3',body='Simple is better than complex.',author=test_user1)
    post4 = Post(title='Complex',body='Complex is better than complicated. ',author=test_user2)
    post5 = Post(title='Flat',body='Flat is better than nested. ',author=test_user2)
    post6 = Post(title='Sparse',body='Sparse is better than dense. ',author=test_user3)
    post7 = Post(title='Readability',body='Readability counts. ',author=test_user4)
    post8 = Post(title='Special',body='Special cases aren\'t special enough to break the rules. ',author=test_user4)

    db.session.add(admin_user)
    db.session.add(test_user1)
    db.session.add(test_user2)
    db.session.add(test_user3)
    db.session.add(test_user4)

    db.session.add(post1)
    db.session.add(post2)
    db.session.add(post3)
    db.session.add(post4)
    db.session.add(post5)
    db.session.add(post6)
    db.session.add(post7)
    db.session.add(post8)
    
    db.session.commit()


if __name__ == '__main__':
    if sys.argv[1] == 'newdb':
        db.drop_all()
        db.create_all()

    init_db()