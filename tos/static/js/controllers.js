"use strict";


tosApp.controller("IndexCtrl", ["$scope", "services",
    function($scope, services) {
        var vm = this;
        vm.services = services;
    }
]);


tosApp.controller("TOSCtrl", ["$state", "$scope", "service", "AgreementData",
    function($state, $scope, service, AgreementData) {
        var vm = this;
        
        vm.service = service;
        vm.emailError = false;
        
        // set up defaults
        vm.policies = {};
        angular.forEach(service.terms, function(term) {
            vm.policies[term.policy_name] = term.policy_values[0];
        });

        vm.getOptions = function(term) {
            var options = [];
            angular.forEach(term.policy_values, function(policy_value) {
                options.push({name: policy_value, value: policy_value});
            });
            return options;
        };
        
        vm.submitAgreement = function() {
            if (vm.user) {
                var data = {
                    user: vm.user,
                    service: vm.service.name
                };

                var terms = [];
                angular.forEach(vm.policies, function(value, name) {
                    terms.push({name: name, value: value});
                });

                data.terms = terms;
                AgreementData.postAgreement(data).then(function(agreement) {
                    $state.go("api", {serviceId: vm.service.name, userId: vm.user});
                });
            } else {
                vm.emailError = true;
            }
        };
    }
]);


tosApp.controller("NotMeCtrl", ["$scope", "disabled",
    function($scope, disabled) {
        var vm = this;
        vm.activate = disabled;
        console.log(disabled);
    }
]);


tosApp.controller("ActivateCtrl", ["$scope", "activate",
    function($scope, activate) {
        var vm = this;
        vm.activate = activate;
    }
]);


tosApp.controller("APICtrl", ["$scope", "AgreementData", "serviceId", "userId",
    function($scope, AgreementData, serviceId, userId) {
        var vm = this;

        vm.serviceId = serviceId;
        vm.userId = userId;
        vm.validates = [];

        vm.validateUser = function() {
            if (vm.serviceId && vm.userId) {
                AgreementData.getValidate(vm.serviceId, vm.userId).then(function(data) {
                    var newData = data.data;
                    newData.user = vm.userId;
                    newData.service = vm.serviceId;
                    vm.validates.unshift(newData);
                });
            }
        };
    }
]);
