import unittest
from branches.Y.Analyse_Calculs import distance as d
from branches.Y.Analyse_Calculs import angle as ag


class MyTestCase(unittest.TestCase):

	def setUp(self) :
		self.point1 = (0, 5)
		self.point2 = (15, 5)
		self.point3 = (15, 0)

	def test_something (self) :
		self.assertNotEqual(True, False)

	def test_distance (self) :
		self.assertEqual(15,	d(self.point1, self.point2))
		self.assertEqual(d(self.point1, self.point2),d(self.point2, self.point1))
		self.assertEqual(5,		d(self.point2, self.point3))
		self.assertEqual("15.811388", "{:f}".format(d(self.point1, self.point3)))

	def test_angle (self) :
		self.assertEqual(ag(self.point1, self.point2),ag(self.point2, self.point1))
		self.assertEqual(0,		ag(self.point1, self.point2))
		self.assertEqual(90,	ag(self.point3, self.point2))
		self.assertEqual(-90,	ag(self.point2, self.point3))


	
if __name__ == '__main__':
	unittest.main()