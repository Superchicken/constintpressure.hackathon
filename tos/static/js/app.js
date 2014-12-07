"use strict";


var tosApp = angular.module("tosApp", [
    "ngSanitize",
    "ui.router",
    "ui.bootstrap"]);
    
tosApp.config(["$stateProvider", "$urlRouterProvider",
    function($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise("/");
        
        $stateProvider.state("index", {
            url: "/",
            templateUrl: "static/partials/index.html",
            controller: "IndexCtrl",
            controllerAs: "index",

            //resolve: {}
        })
        .state('index.child', {
            url: "child",
            template: "<div>I am the child</div>"
        });
    }
]);
