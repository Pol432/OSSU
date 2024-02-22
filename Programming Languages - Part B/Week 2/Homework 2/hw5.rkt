;; Programming Languages, Homework 5

#lang racket
(provide (all-defined-out)) ;; so we can put tests in a second file
(require rackunit)
;; definition of structures for MUPL programs - Do NOT change
(struct var  (string) #:transparent)  ;; a variable, e.g., (var "foo")
(struct int  (num)    #:transparent)  ;; a constant number, e.g., (int 17)
(struct add  (e1 e2)  #:transparent)  ;; add two expressions
(struct ifgreater (e1 e2 e3 e4)    #:transparent) ;; if e1 > e2 then e3 else e4
(struct fun  (nameopt formal body) #:transparent) ;; a recursive(?) 1-argument function
(struct call (funexp actual)       #:transparent) ;; function call
(struct mlet (var e body) #:transparent) ;; a local binding (let var = e in body) 
(struct apair (e1 e2)     #:transparent) ;; make a new pair
(struct fst  (e)    #:transparent) ;; get first part of a pair
(struct snd  (e)    #:transparent) ;; get second part of a pair
(struct aunit ()    #:transparent) ;; unit value -- good for ending a list
(struct isaunit (e) #:transparent) ;; evaluate to 1 if e is unit else 0

;; a closure is not in "source" programs but /is/ a MUPL value; it is what functions evaluate to
(struct closure (env fun) #:transparent) 

;; Problem 1
;; racketlist->mupllist
(define (racketlist->mupllist lst)
  (if (null? lst)
      (aunit)
      (apair (car lst) (racketlist->mupllist (cdr lst)))))

;; mupllist->racketlist
(define (mupllist->racketlist mlst)
  (if (aunit? mlst)
      null
      (cons (apair-e1 mlst) (mupllist->racketlist (apair-e2 mlst)))))


;; Problem 2
;; lookup a variable in an environment
;; Do NOT change this function
(define (envlookup env str)
  (cond [(null? env) (error "unbound variable during evaluation" str)]
        [(equal? (car (car env)) str) (cdr (car env))]
        [#t (envlookup (cdr env) str)]))

;; Do NOT change the two cases given to you.  
;; DO add more cases for other kinds of MUPL expressions.
;; We will test eval-under-env by calling it directly even though
;; "in real life" it would be a helper function of eval-exp.
(define (eval-under-env e env)
  (cond [(var? e) 
         (envlookup env (var-string e))]
        [(add? e)
         (let ([v1 (eval-under-env (add-e1 e) env)]
               [v2 (eval-under-env (add-e2 e) env)])
           (if (and (int? v1)
                    (int? v2))
               (int (+ (int-num v1) 
                       (int-num v2)))
               (error "MUPL addition applied to non-number" e)))]
        ;; CHANGE add more cases here
        [(int? e)
         e]
        [(ifgreater? e)
         (let* ([e1 (eval-under-env (ifgreater-e1 e) env)]
                [e2 (eval-under-env (ifgreater-e2 e) env)])
            (if (and (int? e1) (int? e2))
                (if (> (int-num e1) (int-num e2))
                    (eval-under-env (ifgreater-e3 e) env)
                    (eval-under-env (ifgreater-e4 e) env))
                (error "MUPL condition applied to non-number" e)))]
        [(mlet? e)
         (let ([var (eval-under-env (mlet-e e) env)])
           (eval-under-env (mlet-body e) (cons (cons (mlet-var e) var) env)))]
        [(call? e)
         (let* ([funexp (eval-under-env (call-funexp e) env)]
                [actual (if (fun? (call-actual e)) (eval-under-env (call-actual e) env) (eval-under-env (call-actual e) env))])
           (cond [(closure? funexp)
                  (let* ([fun (closure-fun funexp)]
                         [new-env (append (cons (cons (fun-formal fun) actual) (closure-env funexp)) env)])
                    (if (boolean? (fun-nameopt fun))
                        (eval-under-env (fun-body fun) new-env)
                        (eval-under-env (fun-body fun) (cons (cons (fun-nameopt fun) fun) new-env))))]
                 [(fun? funexp)
                  (let* ([fun funexp] [new-env (cons (cons (fun-formal funexp) actual) env)])
                    (if (boolean? (fun-nameopt funexp))
                        (eval-under-env (fun-body fun) new-env)
                        (eval-under-env (fun-body fun) (cons (cons (fun-nameopt fun) fun) new-env))))]
                 [else (error "MUPL call applied to non-closure" e)]))]
        [(apair? e)
         (let ([e1 (eval-under-env (apair-e1 e) env)] [e2 (eval-under-env (apair-e2 e) env)])
           (apair e1 e2))]
        [(fst? e)
         (let ([var (eval-under-env (fst-e e) env)]) (apair-e1 var))]
        [(snd? e)
         (let ([var (eval-under-env (snd-e e) env)]) (apair-e2 var))]
        [(isaunit? e)
         (let ([exp (eval-under-env (isaunit-e e) env)])(if (aunit? exp) (int 1) (int 0)))]
        [(aunit? e) e]
        [(fun? e) (closure env e)]
        [(closure? e) (closure (append (closure-env e) env) (closure-fun e))]
        [else (error "MUPL evauation applied to non-MUPL-expression" e)]))

;; Do NOT change
(define (eval-exp e)
  (eval-under-env e null))

;; Problem 3

(define (ifaunit e1 e2 e3) (mlet "exp" (isaunit e1) (ifgreater (var "exp") (int 0) e2 e3)))

(define (mlet* lstlst e2)
  (cond [(null? lstlst) e2]
        [else (mlet (car (car lstlst)) (cdr (car lstlst))
                    (mlet* (cdr lstlst) e2))]))

(define (ifeq e1 e2 e3 e4) (mlet "x" e1 (mlet "y" e2 (ifgreater (var "x") (var "y") e4 (ifgreater (var "y") (var "x") e4 e3)))))

;; Problem 4

(define mupl-map
  (fun "map" "f"
       (fun "fun" "lst" (ifaunit (var "lst")
                                 (aunit)
                                 (apair (call (var "f") (fst (var "lst")))
                                        (call (var "fun") (snd (var "lst"))))))))

(define mupl-mapAddN 
  (mlet "map" mupl-map
        (fun #f "x" (call (var "map") (fun #f "y" (add (var "y") (var "x")))))))
; Challenge Problem
(struct fun-challenge (nameopt formal body freevars) #:transparent) ;; a recursive(?) 1-argument function

;; We will test this function directly, so it must do
;; as described in the assignment
(define (compute-free-vars e) "CHANGE")

;; Do NOT share code with eval-under-env because that will make
;; auto-grading and peer assessment more difficult, so
;; copy most of your interpreter here and make minor changes
(define (eval-under-env-c e env) "CHANGE")

;; Do NOT change this
(define (eval-exp-c e)
  (eval-under-env-c (compute-free-vars e) null))
