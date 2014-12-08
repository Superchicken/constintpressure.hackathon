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

            resolve: {
                services: ["ServiceData", function(ServiceData) {
                    return ServiceData.getServices().then(function(data) {
                        return data.data.services;
                    });
                }]
            }
        })
        .state('tos', {
            url: "/tos/:serviceId",
            templateUrl: "static/partials/tos.html",
            controller: "TOSCtrl",
            controllerAs: "tos",

            resolve: {
                service: ["$stateParams", "ServiceData", function($stateParams, ServiceData) {
                    return ServiceData.getService($stateParams.serviceId).then(function(data) {
                        var newData = data.data.service;
                        newData.name = $stateParams.serviceId;
                        return newData;
                    });
                }]
            }
        })
        .state('activate', {
            url: "/activate/:agreementId",
            templateUrl: "static/partials/activate.html",
            controller: "ActivateCtrl",
            controllerAs: "activate",

            resolve: {
                activate: ["$stateParams", "AgreementData", function($stateParams, AgreementData) {
                    return AgreementData.putActivate($stateParams.agreementId).then(function(data) {
                        return data.data;
                    });
                }]
            }
        })
        .state('notme', {
            url: "/deactivate/:agreementId",
            templateUrl: "static/partials/activate.html",
            controller: "NotMeCtrl",
            controllerAs: "activate",

            resolve: {
                disabled: ["$stateParams", "AgreementData", function($stateParams, AgreementData) {
                    return AgreementData.deleteNotMe($stateParams.agreementId).then(function(data) {
                        return data.data;
                    });
                }]
            }
        })
        .state('api', {
            url: "/api?serviceId&userId",
            templateUrl: "static/partials/api.html",
            controller: "APICtrl",
            controllerAs: "api",

            resolve: {
                serviceId: ["$stateParams", function($stateParams) {
                    return $stateParams.serviceId
                }],
                userId: ["$stateParams", function($stateParams) {
                    return $stateParams.userId
                }]
            }
        });
    }
]);
