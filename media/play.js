$(document).ready(function() {
	glCurLevel = 0;
	glTimeLeftInLevel = 0;
	glLevelScore = 0;
	glTotalScore = 0;
	glCurQuestion = '';
	glDebugDiv = false;
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
			if(glLevelScore!=args[1]) {
				alert("Scoreboard desync!");
			}
			endLevel();
		} else if(args[0]=="GAME_OVER") {
			if(glLevelScore!=args[1] || glTotalScore!=args[2]) {
				alert("Scoreboard desync!");
			}
			endLevel();
			endGame();
		} else if (args[0]=="WRONG") {
			$("#answerFeedbackField").text(args[1]+" is incorrect.");
			addScore(-1);
		} else if (args[0]=="INVALID_ANSWER") {
			$("#answerFeedbackField").text("Invalid answer.");
		} else if (args[0]=="NO_QUESTION") {
		} else if (args[0]=="CORRECT") {
			$("#answerFeedbackField").text("Correct.");
			addScore(1);
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
													type: 'POST',
													url: 'pollNextLevel',
													success: pollNextLevelCallback,
													data: {sessionID: sessionID}
												});
												dbg("polling next level");
											}
											, 50
											);
	}

	function pollNextLevelCallback(argcsv) {
	// if 'FAIL' --> do nothing
	// if 'SUCCESS' --> levelfield,
	// start polling for next question, stop polling for next level, update UI for in game mode
		args = argcsv.split(",");
		request_status = args[0];
		if (request_status == 'FAIL')
			return;
		setupLevel(args[1], args[2])
		pollNextQuestion(); // start polling for questions
	}
	function pollNextQuestion() {
		pollNextQuestionInterval = setInterval(function() {
										$.ajax( {
											type: 'POST',
											url: 'pollNextQuestion',
											success: pollNextQuestionCallback,
											data: {sessionID: sessionID}
										});
									}, 50);

	}
	function pollNextQuestionCallback(argscsv) {
	// if 'FAIL' (the next question is not ready) --> do nothing
	// if 'SUCCESS' --> update the text for next question; update score
		args = argscsv.split(",");
		request_status = args[0];
		if (request_status == 'FAIL') {
			dbg("pollNextQuestionCallback:FAIL");
			return;
		}
		else if (request_status == 'SUCCESS') {
			glCurQuestion = args[1];
			dbg("glCurQuestion=" + glCurQuestion);
			$('#id_answer').val('')
			$("#questionField").text(""+glCurQuestion);
		}
	}

	function addScore(d) {
		glLevelScore += d;
		glTotalScore += d;
		$("#scoreField").text("Score: "+glLevelScore);
		$("#totalScoreField").text("Total: "+glTotalScore);
	}
	function endLevel() {
		$("#questionField").text("Level "+glCurLevel+" over");
		$('#id_answer').attr("disabled", true);
		$("#nextLevelButton").removeAttr('disabled');
	}
	function setupLevel(lvl, lvlTime)
	{
		glCurLevel = lvl
		glTimeLeftInLevel = lvlTime
		glLevelScore = 0;
		dbg("set time to: "+glTimeLeftInLevel);
		clearInterval(pollNextLevelInterval); // disable the polling for next level if the level starts

		// update UI elements
		$("#levelField").text("Level: " + glCurLevel);
		$("#timerField").text("Timer: " + glTimeLeftInLevel);
		$('#id_answer').removeAttr("disabled");
		$("#scoreField").text("Score: "+glLevelScore);

		// start timer countdown for next level
		updateTimerInterval = setInterval(function() {
									glTimeLeftInLevel -= 1;
									$("#timerField").text("Timer: "+glTimeLeftInLevel);
									if (glTimeLeftInLevel <= 0) {
										clearInterval(pollNextQuestionInterval);
										clearInterval(updateTimerInterval);
										$('#id_answer').val('');
										submitAnswer();
									}
								}, 1000);
	}
	function endGame() {
		$("#questionField").text("Game over");
		$('#nextLevelButton').attr("disabled", true);
	}
	function dbg(str) {
		if (glDebugDiv) {
			txt = $("#debug").html();
			$("#debug").html(str+'<br>'+txt);
		}
		console.log(str);
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
