var module = angular.module('song-box-ng', ['spotify', 'ngAnimate']);

module.directive('songBox', function($http, Spotify) {
    return {
        restrict: 'E',
        template: '<div class="track"><img src={{imgUrl}}></img> {{trackName}} - {{artist}}</div>',
        scope: {
            trackId: '@',
        },
        transclude: true,
        link: function ($scope) {
            Spotify.getTrack($scope.trackId).then(function (track) {
                var images = track.album.images;
                $scope.trackName = track.name
                $scope.artist = track.artists[0].name
                $scope.imgUrl = images[images.length - 1].url
            });
        }
    }
}); 