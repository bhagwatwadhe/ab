import xml.etree.ElementTree as ET
import threading
import time

#class for data storage and application of quicksort algorithm algortihm
class Quicksort:
	
	rno=0;
	name=""
	branch=""

	#initializing data objects
	def __init__(self,rno,name,branch):
		self.rno=rno
		self.name=name
		self.branch=branch

	#quicksort method
	def quickSort(self,alist):
	   self.quickSortHelper(alist,0,len(alist)-1)

	#quickSortHelper method for sorting array concurrently
	def quickSortHelper(self,alist,first,last):
		if first<last:
			splitpoint = self.partition(alist,first,last)
			#creating threads
			t1=threading.Thread(target=self.quickSortHelper, args=(alist,first,splitpoint-1))
			t2=threading.Thread(target=self.quickSortHelper, args=(alist,splitpoint+1,last))
			#starting threads			
			t1.start()
			t2.start()
			#waiting all threads to complete
			t1.join()
			t2.join()
	
	#function for 'dividing' data
	def partition(self,alist,first,last):
		pivotvalue = alist[first]

		leftmark = first+1
		rightmark = last

		done = False
		#quicksort algorithm applied here
		while not done:

			while leftmark <= rightmark and alist[leftmark] <= pivotvalue:
				leftmark = leftmark + 1

			while alist[rightmark] >= pivotvalue and rightmark >= leftmark:
				rightmark = rightmark -1

			if rightmark < leftmark:
				done = True
			else:
				temp = alist[leftmark]
				alist[leftmark] = alist[rightmark]
				alist[rightmark] = temp

		temp = alist[first]
		alist[first] = alist[rightmark]
		alist[rightmark] = temp


		return rightmark


#----main execution starts from here---

datalist = []
tempObj = Quicksort
intlist = []
sortedData = []
obj = Quicksort #initializing object of Quicksort class

#taking input from XML file
tree = ET.parse('data.xml');
root = tree.getroot()

#moving input data from file to list
for student in root.findall("student"):
	tempObj = Quicksort(int(student.find('rno').text),student.find('studName').text,student.find('studBranch').text)
	datalist.append(tempObj);

#copying integer data to another list for sorting
for obj in datalist:
	intlist.append(obj.rno)

#sorting integer data
tempObj = Quicksort(0,"","") #Constructor initialization
tempObj.quickSort(intlist)

#sorting remaining data as per sorted integer data
for rno in intlist:
	for obj in datalist:
		if obj.rno==rno:
			sortedData.append(obj)

i=0

#printing sorted data
print "Student Details"
for obj in sortedData:
	print "---------------"
	print("Roll No.:"+str(obj.rno))
	print("Name:"+obj.name)
	print("Branch:"+obj.branch)
	print "---------------"

#arranging data for writing into XML file
for student in root.iter('student'):
	student.find('rno').text = str(sortedData[i].rno)
	student.find('studName').text = sortedData[i].name
	student.find('studBranch').text = sortedData[i].branch
	i += 1

#writing data to XML file 
tree.write('data.xml')
