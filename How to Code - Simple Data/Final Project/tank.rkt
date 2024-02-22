;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-abbr-reader.ss" "lang")((modname tank) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/image)

(define TANK1
  (overlay/xy (overlay (ellipse 28 8 "solid" "black")       ;tread center
                       (ellipse 30 10 "solid" "green"))     ;tread outline
              5 -14
              (above (rectangle 5 10 "solid" "black")       ;gun
                     (rectangle 20 10 "solid" "black"))))

(define TANK2
  (overlay/xy (overlay (ellipse 37 12 "solid" "black")      ;tread center
                       (ellipse 40 15 "solid" "green"))     ;tread outline
              5 -16
              (above (rectangle 7.5 12.5 "solid" "black")   ;gun
                     (rectangle 30 10 "solid" "black"))))

TANK1

TANK2