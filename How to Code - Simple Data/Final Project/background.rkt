;; The first three lines of this file were inserted by DrRacket. They record metadata
;; about the language level of this file in a form that our tools can easily process.
#reader(lib "htdp-beginner-abbr-reader.ss" "lang")((modname background) (read-case-sensitive #t) (teachpacks ()) (htdp-settings #(#t constructor repeating-decimal #f #t none #f () #f)))
(require 2htdp/image)

(define WIDTH  300)
(define HEIGHT 640)

(define SPACE (bitmap "stars.png"))

(define BACKGROUND
  (place-image
   SPACE
   (/ WIDTH 2) (/ HEIGHT 2)
   (rectangle WIDTH HEIGHT "solid" "Black")))

(define BOSS
  (overlay/xy (overlay
               (ellipse 295  55 "solid" "Light Slate Gray")
               (ellipse 300  60 "solid" "Dark Slate Gray"))               
              75 -40
              (overlay
               (ellipse 132  92 "solid" "Powder Blue")
               (ellipse 140 100 "solid" "Light Cyan"))))

(define CRATER1
  (ellipse 35 25 "solid" "Dark Gray"))
(define CRATER2
  (ellipse 25 15 "solid" "Dark Gray"))
(define CRATER3
  (ellipse 40 20 "solid" "Dark Gray"))
(define CRATER4
  (ellipse 35 20 "solid" "Dark Gray"))

(define MOON
  (place-image
   CRATER1 150 75
   (place-image
    CRATER3 230 45
    (place-image
     CRATER1 75 30
     (place-image
      CRATER2 175 10
      (place-image
       CRATER4 300 25
       (place-image
        CRATER1 350 75 (ellipse (+ WIDTH 100) 150 "solid" "Light Gray"))))))))

(define HEALTH (overlay/align "middle" "middle"
                              (rectangle 285 15 "solid" "green")
                              (rectangle 300 30 "solid" "gray")))

(define MTS
  (place-image
   MOON
   (/ WIDTH 2) HEIGHT
   (place-image
    BOSS
    (/ WIDTH 2) 90
    (place-image
     HEALTH
     (/ WIDTH 2) 15
     BACKGROUND))))

MTS
