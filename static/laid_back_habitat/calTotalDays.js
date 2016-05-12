function orderRoom() {
	var from_date = new Date(document.getElementById("datepicker1").value);
	var to_date = new Date(document.getElementById("datepicker2").value);
	var diff_day = DiffDay(from_date, to_date);

	if (from_date != "Invalid Date" && to_date != "Invalid Date") {
		if (diff_day > 1) {
			var desctipt = "歡迎您，於" + MyDateFormat(from_date) + "到" + MyDateFormat(to_date) + "來玩" + diff_day + "天。<br />祝您玩得開心。"
		}
		else {
			var desctipt = "歡迎您，於" + MyDateFormat(from_date) + "到" + MyDateFormat(to_date) + "來玩" + diff_day + "天。<br/>不跨天數，無須訂房唷！<br />祝您玩得開心。"
		}
	    document.getElementById("reault_order").innerHTML = desctipt;
	}
	else if (from_date == "Invalid Date" && to_date != "Invalid Date") {
		var desctipt = "您要玩幾到哪一天呢？";
    	document.getElementById("reault_order").innerHTML = desctipt;
	}
	else if (from_date != "Invalid Date" && to_date == "Invalid Date") {
		var desctipt = "您要從哪一天開始玩呢？";
    	document.getElementById("reault_order").innerHTML = desctipt;
	}
	else
	{
		var desctipt = "什麼時候過來玩？";
    	document.getElementById("reault_order").innerHTML = desctipt;
	}
};

function MyDateFormat (date) {
	return date.getUTCFullYear() + "年" + (date.getUTCMonth()+1) + "月" + date.getUTCDate() + "日";
};

function DiffDay(from_date, to_date) {
	return  ((to_date.getTime()-from_date.getTime())/24/60/60/1000)+1;
};

// function date (yyyy_mm_dd) {
// 	if (typeof yyyy_mm_dd === "string" && yyyy_mm_dd.length > 1){
// 		this.yyyy = yyyy_mm_dd.substring(0, 4);
// 		this.mm = yyyy_mm_dd.substring(5, 7);
// 		this.dd = yyyy_mm_dd.substring(8, 10);
// 		this.isRight = true;
// 	}
// 	else
// 		this.isRight = false;

// 	this.diff = function (yyyy_mm_dd) {
// 		var diff_date = new date();
// 		diff_date.yyyy = diff(this.yyyy, yyyy_mm_dd.yyyy);
// 		diff_date.mm = diff(this.mm, yyyy_mm_dd.mm);
// 		diff_date.dd = diff(this.dd, yyyy_mm_dd.dd);
// 		return diff_date;
// 	};

// 	this.toString = function () {
// 		return this.yyyy + "-" + this.mm + "-" + this.dd;
// 	};

// 	var diff = function(this_num, num) {
// 		if (this_num >= num)
// 			return this_num - num;
// 		else
// 			return false;
// 	};
// };