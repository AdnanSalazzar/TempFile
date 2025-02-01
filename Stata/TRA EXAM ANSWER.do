import excel "C:\Users\USER\Downloads\tra_test_a.xlsx", firstrow clear

encode a13, gen(religion)

tab religion, matcell(name1) matrow(name2)

mat freq_table = (name2, name1)

putexcel set "C:\Users\USER\Downloads\test_tables_new.xlsx", sheet("Result")
putexcel A2 = matrix(name2)
putexcel B2 = matrix(name1)  


import excel "C:\Users\USER\Downloads\tra_test_a.xlsx", firstrow clear

collapse (count) freq = a01, by(a13)
egen total = sum(freq)
gen percent = freq / total 

export excel a13 freq percent using ///
	"C:\Users\USER\Downloads\test_tables_new.xlsx", sheet("Result") sheetmodify cell(E2) keepcellfmt


	
import excel "C:\Users\USER\Downloads\tra_test_a.xlsx", firstrow clear

collapse (count) freq = a01, by(a14)
egen total = sum(freq)
gen percent = freq / total 

export excel a14 freq percent using ///
	"C:\Users\USER\Downloads\test_tables_new.xlsx", sheet("Result") sheetmodify cell(I2) keepcellfmt 

	
/*	
Prepare bar graph plotting the percent of households across different types of samples and literacy. 
Save the graphs in "test_tables.xlsx".

*/ 

import excel "C:\Users\USER\Downloads\tra_test_a.xlsx", firstrow clear
graph bar (percent), over(Sample_type) name(graph1, replace)

tempfile graphname 
graph export `graphname', as(png) width(600) height(600)
 
putexcel set "C:\Users\USER\Downloads\test_tables_new.xlsx", sheet("Result") modify
putexcel A10 = image(`graphname')












x