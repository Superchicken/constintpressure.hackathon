"use strict";


tosApp.factory("ServiceData", ["$http",
    function($http) {
        return {
            getServices: function() {
                return $http.get("/services/");
            },
            getService: function(serviceId) {
                return $http.get("/services/" + serviceId);
            }
        };
    }
]);


tosApp.factory("AgreementData", ["$http",
    function($http) {
        return {
            postAgreement: function(data) {
                var config = {
                    cache: false,
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    data: data,
                    url: "/agree"
                };
                return $http(config);
            },
            getValidate: function(serviceId, userId) {
                var config = {
                    cache: true,
                    method: "GET",
                    url: "/agree/" + serviceId + '/' + userId
                };
                return $http(config);
            },
            putActivate: function(agreementId) {
                var config = {
                    cache: false,
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    url: "/agree/" + agreementId
                };
                return $http(config);
            },
            deleteNotMe: function(agreementId) {
                var config = {
                    cache: false,
                    method: "DELETE",
                    url: "/agree/notme/" + agreementId
                };
                return $http(config);
            }
        };
    }
]);