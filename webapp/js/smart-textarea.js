angular.module('smart-textarea-ng', [])
.directive('smartTextarea', function($timeout) {
    return {
        restrict: 'E',
        template: '<textarea class="smart-textarea" type="text" ng-model="currentInputValue" ng-change="update()" placeholder="{{placeholder}}"/></textarea>',
        scope: {
            value: '=',
            timeout: '@',
            placeholder: '@'
        },
        transclude: true,
        link: function ($scope) {
            $scope.timeout = parseInt($scope.timeout);
            $scope.$watch('value', function() {
                $scope.currentInputValue = $scope.value;
            })
            $scope.update = function () {
                 if ($scope.pendingPromise) { $timeout.cancel($scope.pendingPromise); }
                 $scope.pendingPromise = $timeout(function () { 
                        $scope.value = $scope.currentInputValue
                        console.log($scope.value)
                    }, $scope.timeout);
            };
        }
    }
}); 