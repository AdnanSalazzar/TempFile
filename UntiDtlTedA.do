	**# Stata Exam 

	gl motherDir "D:\Lab\TDA Test\Answer_Adnan"	
	cd `motherDir'
	use "${motherDir}\DataSet.dta" , replace 
	
	  
	
**# Question One 
	
	// br religion catholic religion_Islam religion_*
	
	// Getting all the religion name Uniques
	
	levelsof religion if religion != ".", local(religions)

	foreach r in `religions' {
    di "`r'"
	}
	
	
	foreach r in `religions' {
		local clean_r = strtoname("religion_`r'")  // Ensure valid variable name
		gen `clean_r' = (religion == "`r'")
	}
	


	
**# Question Two 
	//  br education education_num
	capture drop education_num
	encode education, generate(education_num)
	
	
**# Third Question
	
	export excel using full_time_workers.xlsx if employ_stat == "Working full time", replace firstrow(variables)

	//pwd
	
**# Forth Question 
	collapse (mean) age, by(district)
	cd `motherDir'
	export excel using "mean_age_by_district.xlsx", replace firstrow(variables)


**# Fifth Question 

	* Generate frequency tables and store them
	contract male
	gen freq_male = _freq
	drop _freq

	contract district
	gen freq_district = _freq
	drop _freq

	contract religion
	gen freq_religion = _freq
	drop _freq

		
