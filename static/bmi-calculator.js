/* CALORIES & MACRONUTRIENTS CALCULATOR */

	$('.cals-and-macros-calculator input[name="height-system"]').click(function() {
		var heightUnits = $(this).val();

		if (heightUnits == "meters") {
			$('.cals-and-macros-calculator input[name="height-tens"]').attr("placeholder", "Meters");
			$('.cals-and-macros-calculator input[name="height-units"]').attr("placeholder", "Centimeters");
		}

		else if (heightUnits == "feet") {
			$('.cals-and-macros-calculator input[name="height-tens"]').attr("placeholder", "Feet");
			$('.cals-and-macros-calculator input[name="height-units"]').attr("placeholder", "Inches");
		}
	});

	$('.cals-and-macros-calculator input[name="weight-system"]').click(function() {
		var weightUnits = $(this).val();

		if (weightUnits == "kilos") {
			$('.cals-and-macros-calculator input[name="weight"]').attr("placeholder", "Kilograms");
		}

		else if (weightUnits == "pounds") {
			$('.cals-and-macros-calculator input[name="weight"]').attr("placeholder", "Pounds");
		}
	});

	$('.cals-and-macros-calculator .calc-submit').click(function() {
		var height = 0;
		var heightTens = parseInt($('.cals-and-macros-calculator input[name="height-tens"]').val());
		var heightUnits= parseInt($('.cals-and-macros-calculator input[name="height-units"]').val());
		var heightType = $('.cals-and-macros-calculator input[name="height-system"]:checked').val();
    var weight = parseInt($('.cals-and-macros-calculator input[name="weight"]').val());
		var weightType = $('.cals-and-macros-calculator input[name="weight-system"]:checked').val();
		var calories = 0;
		var age = parseInt($('.cals-and-macros-calculator input[name=age]').val());
		var sex = $('.cals-and-macros-calculator input[name=sex]:checked').val();
		var job = $('.cals-and-macros-calculator input[name=activity]:checked').val();
    var goal = $('.cals-and-macros-calculator input[name=goal]:checked').val();
    var carbs = 0;
    var protons = 0;
    var fats = 0;

        if (isNaN(age) || isNaN(heightTens) || isNaN(weight)) {
            $('.cals-and-macros-calculator .calc-answer').show(0).html('<span style="color: #a30000;">Please enter values for all the fields.</span>').addClass('animated flipInX').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
            $(this).removeClass('animated flipInX');
            });
        }

        else {
            if(isNaN(heightUnits)) {
                heightUnits = 0;
            }

            if (heightType == "feet") {
                height = ((heightTens * 30.48) + (heightUnits * 2.54));
            }
            else {
                height = (heightTens * 100) + heightUnits;
            }

            if (weightType == "pounds") {
                weight = (weight * 0.453592);
            }

            if (sex == "M") {
                calories = ((weight * 10) + (height * 6.25) - (age * 5) + 5);
            }
            else {
                calories = ((weight * 10) + (height * 6.25) - (age * 5) - 161);
            }

            switch (job) {
                case "L":
                    calories = Math.round(calories * 1.1);
                    break;
                case "M":
                    calories = Math.round(calories * 1.3);
                    break;
                case "V":
                    calories = Math.round(calories * 1.5);
                    break;
                case "E":
                    calories = Math.round(calories * 1.7);
                    break;
            }

            switch (goal) {
                case "fat-loss":
                    if (calories <= 2000) calories = Math.round(0.9 * calories);
                    if (calories > 2000) calories = Math.round(0.8 * calories);
                    carbs = Math.round(0.40 * calories / 4);
                    protons = Math.round(0.40 * calories / 4);
                    fats = Math.round(0.20 * calories / 9);
                    break;
                case "maintenance":
                    carbs = Math.round(0.45 * calories / 4);
                    protons = Math.round(0.30 * calories / 4);
                    fats = Math.round(0.25 * calories / 9);
                    break;
                case "gainz":
                    calories += 500;
                    carbs = Math.round(0.45 * calories / 4);
                    protons = Math.round(0.30 * calories / 4);
                    fats = Math.round(0.25 * calories / 9);
                    break;
            }


            $('.cals-and-macros-calculator .calc-answer').show(0).html('<div>Target  Daily Caloric Intake: <span class="extra-condensed-regular">' + calories + ' calories</span><br>Carbs: <span class="calories extra-condensed-regular">' + carbs + ' G per day.</span><br>Protein: <span class="calories extra-condensed-regular">' + protons + ' G per day.</span><br>Fats: <span class="calories extra-condensed-regular">' + fats + ' G per day.</span></div>').addClass('animated flipInX').one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
                $(this).removeClass('animated flipInX');
            });
        }
    });

});