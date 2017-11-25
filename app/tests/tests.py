import unittest
from ..mod_user.tests import UserTestCase
from ..mod_blog.tests import BlogTestCase


def user_test_suite():
	user_suite = unittest.TestLoader().loadTestsFromTestCase(UserTestCase)
	return user_suite

def blog_test_suite():
	blog_suite = unittest.TestLoader().loadTestsFromTestCase(BlogTestCase)
	return blog_suite

if __name__ == '__main__':
	
	runner = unittest.TextTestRunner()
	user_tests = user_test_suite()
	blog_tests = blog_test_suite()
	print "\n\n\n.......Running User Test Suite..........\n\n\n"
	runner.run(user_tests)
	print "\n\n\n.......Running Blog Test Suite..........\n\n\n"
	runner.run(blog_tests)	