var examplePoems = [
    {text: "If I can't\nLet it go\nOut of my mind"},
    {text: "Don't Stop The Music\nPump It Up\nKeep It Goin' Louder\nIt's What I Want\nDon't Listen To The Radio"},
    {text: "Time frozen\nwhen I Live My Dream\nNo One Sleeps\nWhen I'm Alive"},
    {text: "Help I'm Alive\nAsleep Alone\nThe World Has Turned And Left Me Here\nLeft Me For Dead"},
];

var app = angular.module('spotify-poem', ['song-box-ng', 'smart-textarea-ng', 'ngAnimate']);

app.controller('PoemCtrl', ['$scope', '$http',
    function ($scope, $http) {
        $scope.poem = null;
        $scope.playlist = null;
        $scope.playlist_raw = null;
        $scope.date = new Date();
        $scope.inspirations = examplePoems;        
        
        $scope.poemChanged = function() {
            params = {'q': $scope.poem}
            $http.get('/api/spotifize', {'params': params})
                .success(function (data) {
                    $scope.playlist_raw = JSON.stringify(data)
                    $scope.playlist = data.playlist;
                });
        };

        $scope.pasteInspiration = function(inspiration) {
            $scope.poem = inspiration.text;
        }

        $scope.$watch('poem', $scope.poemChanged)
    }]);

