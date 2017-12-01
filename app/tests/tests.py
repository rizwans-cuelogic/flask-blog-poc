import unittest
from ..mod_user.tests import UserTestCase
from ..mod_blog.tests import BlogTestCase
from ..mod_blog.comment_tests import CommentTests

def user_test_suite():
	user_suite = unittest.TestLoader().loadTestsFromTestCase(UserTestCase)
	return user_suite

def blog_test_suite():
	blog_suite = unittest.TestLoader().loadTestsFromTestCase(BlogTestCase)
	return blog_suite

def comment_test_suite():
	comment_suite = unittest.TestLoader().loadTestsFromTestCase(CommentTests)
	return comment_suite	

if __name__ == '__main__':
	
	runner = unittest.TextTestRunner()
	user_tests = user_test_suite()
	blog_tests = blog_test_suite()	
	comment_tests = comment_test_suite()

	print "\n\n\n.......Running User Test Suite..........\n\n\n"
	runner.run(user_tests)
	print "\n\n\n.......Running Blog Test Suite..........\n\n\n"
	runner.run(blog_tests)
	print "\n\n\n.......Running comment Test Suite..........\n\n\n"
	runner.run(comment_tests)