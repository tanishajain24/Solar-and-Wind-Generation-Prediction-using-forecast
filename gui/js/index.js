let {PythonShell} = require('python-shell')
const path = require('path')

const options = {
		scriptPath: path.join(__dirname, '/../engine/')
	}

$('.ui.selection.dropdown')
  .dropdown()
;



getGeneration = () => {
	const plant = $("#plant").dropdown('get value');
	const city = "London"
	const options = {
		scriptPath: path.join(__dirname, '/../engine/'),
		args: [plant, city]
	}

	predictor = new PythonShell('prediction.py', options)

	predictor.on('message', function(message) {
		console.log(message)
	})


	console.log(plant)
}

$("#predict").on("click", function(){
  getGeneration();
});
