$(document).ready(function() {
	curLevel = 0;
	timeLeftInLevel = 0;
	levelScore = 0;
	totalScore = 0;
	$('#id_answer').attr("disabled", true);

	function submitAnswer() {
		if($('#id_answer').attr("disabled")) return;
		$.ajax({
			type: 'POST',
			url: "submitAnswer",
			success: submitAnswerCallback,
			data: {sessionID: sessionID, answer: $("#id_answer").val()}
		});
		$('#id_answer').val('');
	}

	function submitAnswerCallback(argcsv) {
		args = argcsv.split(",");
		if(args[0]=="LEVEL_OVER") {
			endLevel();
		} else if(args[0]=="GAME_OVER") {
			endLevel();
			endGame();
		} else if (args[0]=="WRONG") {
			$("#answerFeedbackField").text(args[1]+" is incorrect.");
			addScore(-1);
		} else if (args[0]=="INVALID_ANSWER") {
			$("#answerFeedbackField").text("Invalid answer.");
		} else if (args[0]=="NO_QUESTION") {
		} else {
			$("#answerFeedbackField").text("Correct.");
			addScore(1);
			$("#questionField").text(args[0]);
		}
	}

	function playerReady() {
		$.ajax({
			type: 'POST',
			url: "playerReady",
			success: pollNextLevel,
			data: {sessionID: sessionID}
		});
	}

	function pollNextLevel() {
		$("#nextLevelButton").attr("disabled", true);
		pollNextLevelInterval = setInterval(
											function() {
												$.ajax({
													type: 'GET',
													url: 'pollNextLevel',
													//success: function(a) { console.log(a) },//console.log(''),//pollNextLevelCallback,
													success: pollNextLevelCallback,
													data: {sessionID: sessionID}
												});
												dbg("polling next level");
											}
											, 500
											);
	}

	/*
	*/
	function pollNextLevelCallback(argcsv) {
	// if 'FAIL' --> do nothing
	// if 'SUCCESS' --> levelfield,
	// start polling for next question, stop polling for next level, update UI for in game mode
		args = argcsv.split(",");
		request_status = args[0];
		if (request_status == 'FAIL')
			return;
		//debug(
		clearInterval(pollNextLevelInterval); // disable the polling for next level if the level starts
		curLevel = args[1];
		curLevelTime = args[2];
		curLevelScore = 0;

		$("#levelField").text("Level: " + curLevel);
		$("#timerField").text("Timer: " + curLevelTime);
		$('#id_answer').removeAttr("disabled");
		$("#scoreField").text("Score: "+levelScore);
		// start timer countdown for next level
		updateTimerInterval = setInterval(function() {
									curLevelTime -= 1;
									$("#timerField").text("Timer: "+curLevelTime);
								}, 1000);
		pollNextQuestion(); // start polling for questions
	}
	function pollNextQuestion() {
		pollNextQuestionInterval = setInterval(function() {
										$.ajax( {
											type: 'GET',
											url: 'pollNextQuestion',
											success: pollNextQuestionCallback,
											//success: function(a) {console.log(a)},//console.log("",a)},
											data: {sessionID: sessionID}
										});
									}, 500);

		//TODO refactor to end level method::
		if (curLevelTime <= 0) {
			clearInterval(pollNextQuestionInterval);
			clearInterval(updateTimerInterval);
			$('#id_answer').val('');
			submitAnswer(); //TODO check this
		}
	}
	function pollNextQuestionCallback(argscsv) {
	// if 'FAIL' (the next question is not ready) --> do nothing
	// if 'SUCCESS' --> update the text for next question; update score
		args = argscsv.split(",");
		request_status = args[0];
		console.log(argscsv+" "+args+" "+request_status)
		if (request_status == 'FAIL')
			dbg("pollNextQuestionCallback FAIL");
		else {
			curQuestion = args[1];
			dbg("curQuestion= " + curQuestion);
			$("#questionField").text("Question:" + curQuestion);
			addScore(1);
		}
	}

	function addScore(d) {
		levelScore += d;
		totalScore += d;
		$("#scoreField").text("Score: "+levelScore);
		$("#totalScoreField").text("Total: "+totalScore);
	}
	function endLevel() {
		if(levelScore!=args[1]) {
			alert("Scoreboard desync!");
		}
		$("#questionField").text("Level "+curLevel+" over");
		$('#id_answer').attr("disabled", true);
	}
	function endGame() {
		$("#questionField").text("Game over");
		$('#nextLevelButton').attr("disabled", true);
	}
	function dbg(str) {
		txt = $("#debug").text();
		$("#debug").text(str+"\n"+txt);
	}



	// Bind button listeners
	$("#id_answer").keydown(function(event) {
		if (event.keyCode == 13 || event.keyCode == 32) {
			submitAnswer();
		} 
	});
	$("#nextLevelButton").click(function(event) {
		playerReady();
	});
	
}); // end Docuemnt.Ready
