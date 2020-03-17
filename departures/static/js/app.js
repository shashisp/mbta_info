var app = angular.module('mbta', ["restangular"]);

app.config(function($interpolateProvider, $httpProvider, RestangularProvider){
  
    $interpolateProvider.startSymbol("[[");
    $interpolateProvider.endSymbol("]]");

    RestangularProvider.setBaseUrl('');

    });

app.controller('ScheduleCtrl', function($scope, Restangular) {


  $scope.query = 'place-north'; //inital value

  $scope.current_date = new Date();

  $scope.current_time = new Date()

  $scope.loadData = function(){
    var url = 'api/?station='+$scope.query;
    var resource = Restangular.all(url);
        
    resource.getList().then(function(data){
        $scope.results = data;
    });
  }

  setInterval(function(){
    $scope.loadData();
  }, 30000)

  $scope.loadData();
});