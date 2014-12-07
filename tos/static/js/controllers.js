"use strict";


tosApp.controller("IndexCtrl", ["$scope",
    function($scope) {
        var vm = this;
        
        vm.temp = 'my temp string';
        
        vm.test = function () {
            return false;
        };
        
        vm.myList = [1,2,3,4,5]; 
    }
]);