// TDA EXAM

	gl nbhd	"D:\Lab\Stata"
	cd "${nbhd}"
	
	
	import excel "tra_test_a-1", firstrow clear
	save file1.dta, replace


	import excel "tra_test_b-1", firstrow clear
	save file2.dta, replace

	use file1.dta, clear
	merge 1:m a01 using file2.dta
	

	** making the frequeency table in STATA

	encode a13 , gen(religion) 
	encode Sample_type , gen(sample_types_num)
	encode marital_status , gen(marital_status_num)
	tabulate religion  marital_status_num, matcell(name1) matrow(name2) 
	
	matrix list name1
	matrix list name2
	
	
	// putting into excel 
	
	putexcel set "${nbhd}\test_tables.xlsx" , sheet("Result") modify
	putexcel A2 = matrix(name2)
	putexcel B2 = matrix(name1)
	
	
	
	// finding frequeency in another way ///////////////////////
	collapse (count) freq = a01 , by(a13 marital_status)
	
	** now finiding sum 
	
	egen total = sum(freq)
	
	gen percentage = freq / total 
	
	export excel a13 freq percentage using "${nbhd}\test_tables.xlsx" , sheet("Result" , modify)  cell(E2)
	
	
	////////Second Question 
	// getting all the names of the religion 
	
	
	
	**tabulate marital_status a13 
	
	
	// making the graph 
	
	// this show the distinct values 
	//levels Sample_type
	
	///SECOND QUESTION
	
	gl nbhd	"D:\Lab\Stata"
	cd "${nbhd}"
	
	
	import excel "tra_test_a-1", firstrow clear
	save file1.dta, replace


	import excel "tra_test_b-1", firstrow clear
	save file2.dta, replace

	use file1.dta, clear
	merge 1:m a01 using file2.dta
	
	levelsof Sample_type, local(sample_types)
	
	// display "`sample_types'
	
	encode literacy, gen(literacy_num)
	levels literacy_num
	
	
	graph bar (percent) literacy_num, over(Sample_type, label(labsize(vsmall))) ///
    bar(1, lcolor(blue)) ///
    title("Percentage of Households by Literacy and Sample Type")
	
//	
// 	tabulate Sample_type literacy
//	
// 	graph bar (percent) literacy_num, over(Sample_type) over(literacy) ///
//     bar(1, lcolor(blue)) ///
//     title("Percentage of Households by Literacy and Sample Type")

	graph bar (percent) literacy_num, over(Sample_type) ///
    by(literacy, total) ///
    bar(1, lcolor(blue)) ///
    title("Percentage of Households by Literacy and Sample Type")

	
	
	
	
	
	
	
	
	
	
	
	
	
	