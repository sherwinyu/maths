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
			data: {sessID: sessionID, answer: $("#id_answer").val()}
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
	
	function startLevel() {
		$.ajax({
			type: 'POST',
			url: "newLevel",
			success: startLevelCallback,
			data: {sessID: sessionID}
		});
	}
	function startLevelCallback(argcsv) {
		args = argcsv.split(",");
		curLevel = args[0];
		$("#levelField").text("Level: "+curLevel);
		timeLeftInLevel = args[1];
		$("#timerField").text("Timer: "+timeLeftInLevel);
		timerInterval = setInterval(function() {
			timeLeftInLevel-=1;
			$("#timerField").text("Timer: "+timeLeftInLevel);
			if(timeLeftInLevel<=0) {
				clearInterval(timerInterval);
				$('#id_answer').val('');
				submitAnswer();
			}
		}, 1000);
		$("#questionField").text(args[2]);
		$('#id_answer').removeAttr("disabled");
		levelScore=0
		$("#scoreField").text("Score: "+levelScore);
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
	
	$("#id_answer").keydown(function(event) {
		if (event.keyCode == 13 || event.keyCode == 32) {
			submitAnswer();
		} 
	});
	$("#nextLevelButton").click(function(event) {
		startLevel();
	});
	
});