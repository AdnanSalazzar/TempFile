//  The Assignment 

	gl nbhd	"main_neighborhood_list_wave1.csv"


	insheet using "${nbhd}", names clear

		
	

		generate area_code = . 
		generate area_label = ""  

		replace area_code = cond(main, 1, ///
								cond(chittagong, 2, ///
								cond(comilla_south, 3, ///
								cond(comilla_north, 4, ///
								cond(naryanganj_east, 5, ///
								cond(narsingdi, 6, ///
								cond(dhamrai, 7, ///
								cond(bhaluka, 8, ///
								cond(gazipur_north, 9, .)))))))))

		
		replace area_label = cond(main, "main", ///
								 cond(chittagong, "chittagong", ///
								 cond(comilla_south, "comilla_south", ///
								 cond(comilla_north, "comilla_north", ///
								 cond(naryanganj_east, "naryanganj_east", ///
								 cond(narsingdi, "narsingdi", ///
								 cond(dhamrai, "dhamrai", ///
								 cond(bhaluka, "bhaluka", ///
								 cond(gazipur_north, "gazipur_north", "")))))))))


		
		generate byte area_code = . 
		generate area_label = ""  

		replace area_code = 1 if main == 1
		replace area_label = "main" if main == 1

		replace area_code = 2 if chittagong == 1
		replace area_label = "chittagong" if chittagong == 1

		replace area_code = 3 if comilla_south == 1
		replace area_label = "comilla_south" if comilla_south == 1

		replace area_code = 4 if comilla_north == 1
		replace area_label = "comilla_north" if comilla_north == 1

		replace area_code = 5 if naryanganj_east == 1
		replace area_label = "naryanganj_east" if naryanganj_east == 1

		replace area_code = 6 if narsingdi == 1
		replace area_label = "narsingdi" if narsingdi == 1

		replace area_code = 7 if dhamrai == 1
		replace area_label = "dhamrai" if dhamrai == 1

		replace area_code = 8 if bhaluka == 1
		replace area_label = "bhaluka" if bhaluka == 1

		replace area_code = 9 if gazipur_north == 1
		replace area_label = "gazipur_north" if gazipur_north == 1

x




		// keep if main == 1 | chittagong == 1 | comilla_south == 1 | comilla_north == 1 | ///
		//          naryanganj_east == 1 | narsingdi == 1 | dhamrai == 1 | bhaluka == 1 | ///
		//          gazipur_north == 1
		//		 

		keep if main > 0 | backup > 0
				 
		export excel "processed_data1.xlsx", firstrow(variables) replace



		xx