import xlrd
import boto3

def read_time_table(kidname):
	
	time_table_string = kidname + ", Your time table is"
	s3 = boto3.client('s3')

	s3.download_file('s00bucket', 'timetable.xlsx', '/tmp/timetable.xlsx')
	workbook = xlrd.open_workbook('/tmp/timetable.xlsx')
	worksheet = workbook.sheet_by_name(kidname)
	num_rows = worksheet.nrows - 1
	curr_row = 0
	while (curr_row < num_rows):
		curr_row = curr_row + 1
		time_table_string += ", "
		time_table_string = time_table_string + worksheet.cell(curr_row,3).value
	return (time_table_string)
