import csv
from validate_email import validate_email
import csvFilePath

filePath = csvFilePath.getPath()
print filePath

with open(filePath, 'r') as f:
	with open('./output.csv', 'w') as output:
		# define writer
		writer = csv.writer(output, lineterminator = "\n")
		# create reader
		address_list = csv.reader(f)
		output_list = []
		row = next(address_list)
		row.append('email_valid')
		output_list.append(row)
		for row in address_list:
			email = row[5]
			is_valid = validate_email(email, check_mx = True)
			row.append(is_valid)
			output_list.append(row)



''' checking if email exists and store in dict
myDict = dict()
from validate_email import validate_email
for email in email_list[0:10]:
	is_valid = validate_email(email, check_mx = True)
	myDict[validate_email] = is_valid
	print 'Checking: ', email, 'Exists: ', is_valid
'''

''' make frequency table from email ending
# split email addresses by @ to get the email ending
email_ending = []
for email in email_list:
	email.lower()
	email = email.split('@')
	email_ending.append(email[1:])

# last process returns a list of list
# next task converts this list of list to a list with strings 

x = []
for a in email_ending:
	for b in a:
		x.append(b[0:])
email_ending = x


counts = dict()	
for element in email_ending:
	if element not in counts:
		counts[element] = 1
	else:
		counts[element] += 1

# sort dict by value
lst = list()
for key, val in counts.items():
	lst.append( (val, key) )

lst.sort(reverse = True)
myDict = dict()
for key, val in lst[:10]:
	 myDict[val] = key

lst = myDict

print lst
'''

