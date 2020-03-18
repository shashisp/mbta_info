var app = angular.module('mbta', ["restangular"]);

app.config(function($interpolateProvider, $httpProvider, RestangularProvider){
  
    $interpolateProvider.startSymbol("[[");
    $interpolateProvider.endSymbol("]]");

    RestangularProvider.setBaseUrl('');

    });

app.controller('ScheduleCtrl', function($scope, Restangular) {

    $scope.getCurrentTime = function() {
        let today     = new Date();
        let hours    = today.getHours();
        let minutes  = today.getMinutes();

        let ampm = hours >= 12 ? 'pm' : 'am';

        hours = hours % 12;
        hours = hours ? hours : 12;
        minutes = minutes < 10 ? '0'+minutes : minutes;
        let currentTime = hours + ':' + minutes + ' ' + ampm;
        return currentTime;
    }


    $scope.query = 'place-north'; //inital value

    let today = new Date();
    let dd = today.getDate();

    let mm = today.getMonth()+1; 
    let yyyy = today.getFullYear();
    
    if(dd<10) 
        {
            dd='0'+dd;
        } 

    if(mm<10) 
    {
        mm='0'+mm;
    }

    $scope.current_date = mm+'-'+dd+'-'+yyyy;
    $scope.current_day_name = today.toString().split(' ')[0];

    $scope.current_time = $scope.getCurrentTime();

    $scope.loadData = function(){
        let url = 'api/?station='+$scope.query;
        let resource = Restangular.all(url);
        
        resource.getList().then(function(data){
            $scope.results = data;
        });
    }

      setInterval(function(){
        $scope.loadData();
        $scope.current_time = $scope.getCurrentTime();
      }, 30000)

    $scope.loadData();
});