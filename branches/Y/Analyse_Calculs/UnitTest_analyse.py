import unittest
import cv2
from .analyse import analyse


class MyTestCase(unittest.TestCase):
	def setup(self) :
		cam1 = cv2.imread("vue_cam_1.jpg", cv2.IMREAD_COLOR)
		cam2 = cv2.imread("vue_cam_2.jpg", cv2.IMREAD_COLOR)
		cam3 = cv2.imread("surex.jpg", cv2.IMREAD_COLOR)
		cam4 = cv2.imread("surex2.jpg", cv2.IMREAD_COLOR)
		cam5 = cv2.imread("plan.jpg", cv2.IMREAD_COLOR)


	def test_analyse(self) :
		self.assertEquals("", analyse(self.cam1))
		self.assertEquals("", analyse(self.cam2))
		self.assertEquals("", analyse(self.cam3))
		self.assertEquals("", analyse(self.cam4))
		self.assertEquals("", analyse(self.cam5))

	

if __name__ == '__main__':
	unittest.main()
