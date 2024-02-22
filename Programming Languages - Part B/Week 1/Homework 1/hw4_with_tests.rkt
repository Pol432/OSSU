#lang racket

(require rackunit)

;; Sequence
(define (sequence low high stride)
  (let [(sum (+ low stride))]
  (if (> low high)
      null
      (cons low (sequence sum high stride)))))

;; TESTS
(check-equal? (sequence 0  5 1) (list 0 1 2 3 4 5))
(check-equal? (sequence 3 11 2) (list 3 5 7 9 11))
(check-equal? (sequence 3  8 3) (list 3 6))
(check-equal? (sequence 3  2 1) null)


;; String-append-map
(define (string-append-map lst suf)
  (map (lambda (str) (string-append str suf)) lst))

;; TESTS
(check-equal? (string-append-map (list "dan" "dog" "curry" "dog2") ".jpg") '("dan.jpg" "dog.jpg" "curry.jpg" "dog2.jpg") "string-append-map test")
(check-equal? (string-append-map (list "p" "s" "u") "no") (list "pno" "sno" "uno"))
(check-equal? (string-append-map (list "a" "b") "d") (list "ad" "bd"))
(check-equal? (string-append-map null "no") null)


;; list-nth-mod
(define (list-nth-mod lst n) 0
  (cond [(< n 0) (error "list-nth-mod: negative number")]
        [(empty? lst) (error "list-nth-mod: empty list")]
        [else (list-ref lst (remainder n (length lst)))]))

;; TESTS
(check-equal? (list-nth-mod (list 0 1 2 3 4) 2) 2 "list-nth-mod test")
(check-equal? (list-nth-mod (list "hi" 1) 2) "hi")
(check-equal? (list-nth-mod (list 0 1 "no" 3) 5) 1)


;; stream-for-n-steps
(define (stream-for-n-steps st num)
  (if (= num 0)
      null
      (cons (car (st)) (stream-for-n-steps (cdr (st)) (- num 1)))))

;; TESTS
(define ones (lambda () (cons 1 ones)))
(define twos
  (letrec ([f (lambda (x) (cons x (lambda () (f (* x 2)))))])
    (lambda () (f 2))))
(check-equal? (stream-for-n-steps ones 2) (list 1 1))
(check-equal? (stream-for-n-steps twos 4) (list 2 4 8 16))


;; funny-number-stream
(define funny-number-stream
  (letrec ([f (λ (x) (cons (negate x) (lambda () (f (+ x 1)))))]
           [negate (λ (x) (if (= (remainder x 5) 0) (* -1 x) x))])
    (λ () (f 1))))

;; TESTS
(check-equal? (stream-for-n-steps funny-number-stream 16) (list 1 2 3 4 -5 6 7 8 9 -10 11 12 13 14 -15 16))
(check-equal? (stream-for-n-steps funny-number-stream 10) (list 1 2 3 4 -5 6 7 8 9 -10))
(check-equal? (stream-for-n-steps funny-number-stream  0) null)


;; dan-then-dog
(define dan-then-dog
  (letrec ([f (λ (x) (cons (select x) (λ () (f (+ x 1)))))]
           [select (λ (x) (if (odd? x) "dan.jpg" "dog.jpg"))])
    (λ () (f 1))))

;; TESTS
(check-equal? (stream-for-n-steps dan-then-dog  1) (list "dan.jpg"))
(check-equal? (stream-for-n-steps dan-then-dog 10) (list "dan.jpg" "dog.jpg" "dan.jpg" "dog.jpg" "dan.jpg" "dog.jpg" "dan.jpg" "dog.jpg" "dan.jpg" "dog.jpg"))


;; stream-add-zero
(define (stream-add-zero st)
  (letrec ([f (λ (s) (cons (cons 0 (car (s))) (λ () (f (cdr (s))))))])
    (λ () (f st))))

;; TEST
(check-equal? (stream-for-n-steps (stream-add-zero ones) 1) (list (cons 0 1)))
(check-equal? (stream-for-n-steps (stream-add-zero twos) 4) (list (cons 0 2) (cons 0 4) (cons 0 8) (cons 0 16)))


;; cycle-lists
(define (cycle-lists xs ys)
  (letrec ([f (λ (x) (cons (cons (list-nth-mod xs x) (list-nth-mod ys x)) (λ () (f (+ x 1)))))])
    (λ () (f 0))))

;; TESTS
(check-equal? (stream-for-n-steps (cycle-lists (list 1 2 3) (list "a" "b")) 3) (list (cons 1 "a") (cons 2 "b") (cons 3 "a")))
(check-equal? (stream-for-n-steps (cycle-lists (list 4 5) (list 2 1)) 2) (list (cons 4 2) (cons 5 1)))


;; vector-assoc
(define (vector-assoc v vec)
  (letrec ([len (vector-length vec)]
           [f (λ (loc) (if (>= loc len) #f (let ([cur (vector-ref vec loc)])
                                            (if (equal? (car cur) v) cur (f (+ loc 1))))))])
    (f 0)))

;; TESTS
(check-equal? (vector-assoc 4    (vector (cons 2 1) (cons 3 1) (cons 4 1) (cons 5 1))) (cons 4 1))
(check-equal? (vector-assoc "hi" (vector (cons "" 4) (cons 3 "hi") (cons "hi" 2)))     (cons "hi" 2))
(check-equal? (vector-assoc 4    (vector (cons 2 1) (cons 3 1) (cons 0 1) (cons 5 1))) #f)


;; cached-assoc
(define (cached-assoc lst n)
  (letrec ([cache (make-vector n #f)]
           [f (λ (x)
                (let ([ans (vector-assoc x cache)])
                  (if ans
                      (cdr ans)
                      (let ([new-ans (assoc ans lst)])
                        (begin
                          (vector-set! cache 1)
                          new-ans)))))])
    (lambda (v) (assoc v lst))))
;; TESTS
(check-equal? ((cached-assoc (list (cons 1 2) (cons 3 4)) 3) 3) (cons 3 4))








;; Sequence
;; TESTS
(check-equal? (sequence 0  5 1) (list 0 1 2 3 4 5))
(check-equal? (sequence 3 11 2) (list 3 5 7 9 11))
(check-equal? (sequence 3  8 3) (list 3 6))
(check-equal? (sequence 3  2 1) null)


;; String-append-map
;; TESTS
(check-equal? (string-append-map (list "dan" "dog" "curry" "dog2") ".jpg") '("dan.jpg" "dog.jpg" "curry.jpg" "dog2.jpg") "string-append-map test")
(check-equal? (string-append-map (list "p" "s" "u") "no") (list "pno" "sno" "uno"))
(check-equal? (string-append-map (list "a" "b") "d") (list "ad" "bd"))
(check-equal? (string-append-map null "no") null)


;; list-nth-mod
;; TESTS
(check-equal? (list-nth-mod (list 0 1 2 3 4) 2) 2 "list-nth-mod test")
(check-equal? (list-nth-mod (list "hi" 1) 2) "hi")
(check-equal? (list-nth-mod (list 0 1 "no" 3) 5) 1)


;; stream-for-n-steps
;; TESTS
(check-equal? (stream-for-n-steps ones 2) (list 1 1))
(check-equal? (stream-for-n-steps twos 4) (list 2 4 8 16))


;; funny-number-stream
;; TESTS
(check-equal? (stream-for-n-steps funny-number-stream 16) (list 1 2 3 4 -5 6 7 8 9 -10 11 12 13 14 -15 16))
(check-equal? (stream-for-n-steps funny-number-stream 10) (list 1 2 3 4 -5 6 7 8 9 -10))
(check-equal? (stream-for-n-steps funny-number-stream  0) null)


;; dan-then-dog
;; TESTS
(check-equal? (stream-for-n-steps dan-then-dog  1) (list "dan.jpg"))
(check-equal? (stream-for-n-steps dan-then-dog 10) (list "dan.jpg" "dog.jpg" "dan.jpg" "dog.jpg" "dan.jpg" "dog.jpg" "dan.jpg" "dog.jpg" "dan.jpg" "dog.jpg"))




;; TEST
(check-equal? (stream-for-n-steps (stream-add-zero ones) 1) (list (cons 0 1)))
(check-equal? (stream-for-n-steps (stream-add-zero twos) 4) (list (cons 0 2) (cons 0 4) (cons 0 8) (cons 0 16)))

;; TESTS
(check-equal? (stream-for-n-steps (cycle-lists (list 1 2 3) (list "a" "b")) 3) (list (cons 1 "a") (cons 2 "b") (cons 3 "a")))
(check-equal? (stream-for-n-steps (cycle-lists (list 4 5) (list 2 1)) 2) (list (cons 4 2) (cons 5 1)))

;; TESTS
(check-equal? (vector-assoc 4    (vector (cons 2 1) (cons 3 1) (cons 4 1) (cons 5 1))) (cons 4 1))
(check-equal? (vector-assoc "hi" (vector (cons "" 4) (cons 3 "hi") (cons "hi" 2)))     (cons "hi" 2))
(check-equal? (vector-assoc 4    (vector (cons 2 1) (cons 3 1) (cons 0 1) (cons 5 1))) #f)

;; TESTS
(check-equal? ((cached-assoc (list (cons 1 2) (cons 3 4)) 3) 3) (cons 3 4))





