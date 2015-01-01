/* blasp.h  --  C prototypes for BLAS                         Ver 1.0 */
/* Jesse Bennett                                       March 23, 2000 */

/* Functions  listed in alphabetical order */
#include <stdint.h>
#ifndef INT64_DEFINED
typedef int64_t INT64;
#define INT64_DEFINED
#endif

#ifdef F2C_COMPAT

void cdotc_(fcomplex *dotval, INT64 *n, fcomplex *cx, INT64 *incx,
            fcomplex *cy, INT64 *incy);

void cdotu_(fcomplex *dotval, INT64 *n, fcomplex *cx, INT64 *incx,
            fcomplex *cy, INT64 *incy);

double sasum_(INT64 *n, float *sx, INT64 *incx);

double scasum_(INT64 *n, fcomplex *cx, INT64 *incx);

double scnrm2_(INT64 *n, fcomplex *x, INT64 *incx);

double sdot_(INT64 *n, float *sx, INT64 *incx, float *sy, INT64 *incy);

double snrm2_(INT64 *n, float *x, INT64 *incx);

void zdotc_(dcomplex *dotval, INT64 *n, dcomplex *cx, INT64 *incx,
            dcomplex *cy, INT64 *incy);

void zdotu_(dcomplex *dotval, INT64 *n, dcomplex *cx, INT64 *incx,
            dcomplex *cy, INT64 *incy);

#else

fcomplex cdotc_(INT64 *n, fcomplex *cx, INT64 *incx, fcomplex *cy, INT64 *incy);

fcomplex cdotu_(INT64 *n, fcomplex *cx, INT64 *incx, fcomplex *cy, INT64 *incy);

float sasum_(INT64 *n, float *sx, INT64 *incx);

float scasum_(INT64 *n, fcomplex *cx, INT64 *incx);

float scnrm2_(INT64 *n, fcomplex *x, INT64 *incx);

float sdot_(INT64 *n, float *sx, INT64 *incx, float *sy, INT64 *incy);

float snrm2_(INT64 *n, float *x, INT64 *incx);

dcomplex zdotc_(INT64 *n, dcomplex *cx, INT64 *incx, dcomplex *cy, INT64 *incy);

dcomplex zdotu_(INT64 *n, dcomplex *cx, INT64 *incx, dcomplex *cy, INT64 *incy);

#endif

/* Remaining functions listed in alphabetical order */

INT64 caxpy_(INT64 *n, fcomplex *ca, fcomplex *cx, INT64 *incx, fcomplex *cy,
           INT64 *incy);

INT64 ccopy_(INT64 *n, fcomplex *cx, INT64 *incx, fcomplex *cy, INT64 *incy);

INT64 cgbmv_(char *trans, INT64 *m, INT64 *n, INT64 *kl, INT64 *ku,
           fcomplex *alpha, fcomplex *a, INT64 *lda, fcomplex *x, INT64 *incx,
           fcomplex *beta, fcomplex *y, INT64 *incy);

INT64 cgemm_(char *transa, char *transb, INT64 *m, INT64 *n, INT64 *k,
           fcomplex *alpha, fcomplex *a, INT64 *lda, fcomplex *b, INT64 *ldb,
           fcomplex *beta, fcomplex *c, INT64 *ldc);

INT64 cgemv_(char *trans, INT64 *m, INT64 *n, fcomplex *alpha, fcomplex *a,
           INT64 *lda, fcomplex *x, INT64 *incx, fcomplex *beta, fcomplex *y,
           INT64 *incy);

INT64 cgerc_(INT64 *m, INT64 *n, fcomplex *alpha, fcomplex *x, INT64 *incx,
           fcomplex *y, INT64 *incy, fcomplex *a, INT64 *lda);

INT64 cgeru_(INT64 *m, INT64 *n, fcomplex *alpha, fcomplex *x, INT64 *incx,
           fcomplex *y, INT64 *incy, fcomplex *a, INT64 *lda);

INT64 chbmv_(char *uplo, INT64 *n, INT64 *k, fcomplex *alpha, fcomplex *a,
           INT64 *lda, fcomplex *x, INT64 *incx, fcomplex *beta, fcomplex *y,
           INT64 *incy);

INT64 chemm_(char *side, char *uplo, INT64 *m, INT64 *n, fcomplex *alpha,
           fcomplex *a, INT64 *lda, fcomplex *b, INT64 *ldb, fcomplex *beta,
           fcomplex *c, INT64 *ldc);

INT64 chemv_(char *uplo, INT64 *n, fcomplex *alpha, fcomplex *a, INT64 *lda,
           fcomplex *x, INT64 *incx, fcomplex *beta, fcomplex *y, INT64 *incy);

INT64 cher_(char *uplo, INT64 *n, float *alpha, fcomplex *x, INT64 *incx,
          fcomplex *a, INT64 *lda);

INT64 cher2_(char *uplo, INT64 *n, fcomplex *alpha, fcomplex *x, INT64 *incx,
           fcomplex *y, INT64 *incy, fcomplex *a, INT64 *lda);

INT64 cher2k_(char *uplo, char *trans, INT64 *n, INT64 *k, fcomplex *alpha,
            fcomplex *a, INT64 *lda, fcomplex *b, INT64 *ldb, float *beta,
            fcomplex *c, INT64 *ldc);

INT64 cherk_(char *uplo, char *trans, INT64 *n, INT64 *k, float *alpha,
           fcomplex *a, INT64 *lda, float *beta, fcomplex *c, INT64 *ldc);

INT64 chpmv_(char *uplo, INT64 *n, fcomplex *alpha, fcomplex *ap, fcomplex *x,
           INT64 *incx, fcomplex *beta, fcomplex *y, INT64 *incy);

INT64 chpr_(char *uplo, INT64 *n, float *alpha, fcomplex *x, INT64 *incx,
          fcomplex *ap);

INT64 chpr2_(char *uplo, INT64 *n, fcomplex *alpha, fcomplex *x, INT64 *incx,
           fcomplex *y, INT64 *incy, fcomplex *ap);

INT64 crotg_(fcomplex *ca, fcomplex *cb, float *c, fcomplex *s);

INT64 cscal_(INT64 *n, fcomplex *ca, fcomplex *cx, INT64 *incx);

INT64 csscal_(INT64 *n, float *sa, fcomplex *cx, INT64 *incx);

INT64 cswap_(INT64 *n, fcomplex *cx, INT64 *incx, fcomplex *cy, INT64 *incy);

INT64 csymm_(char *side, char *uplo, INT64 *m, INT64 *n, fcomplex *alpha,
           fcomplex *a, INT64 *lda, fcomplex *b, INT64 *ldb, fcomplex *beta,
           fcomplex *c, INT64 *ldc);

INT64 csyr2k_(char *uplo, char *trans, INT64 *n, INT64 *k, fcomplex *alpha,
            fcomplex *a, INT64 *lda, fcomplex *b, INT64 *ldb, fcomplex *beta,
            fcomplex *c, INT64 *ldc);

INT64 csyrk_(char *uplo, char *trans, INT64 *n, INT64 *k, fcomplex *alpha,
           fcomplex *a, INT64 *lda, fcomplex *beta, fcomplex *c, INT64 *ldc);

INT64 ctbmv_(char *uplo, char *trans, char *diag, INT64 *n, INT64 *k,
           fcomplex *a, INT64 *lda, fcomplex *x, INT64 *incx);

INT64 ctbsv_(char *uplo, char *trans, char *diag, INT64 *n, INT64 *k,
           fcomplex *a, INT64 *lda, fcomplex *x, INT64 *incx);

INT64 ctpmv_(char *uplo, char *trans, char *diag, INT64 *n, fcomplex *ap,
           fcomplex *x, INT64 *incx);

INT64 ctpsv_(char *uplo, char *trans, char *diag, INT64 *n, fcomplex *ap,
           fcomplex *x, INT64 *incx);

INT64 ctrmm_(char *side, char *uplo, char *transa, char *diag, INT64 *m,
           INT64 *n, fcomplex *alpha, fcomplex *a, INT64 *lda, fcomplex *b,
           INT64 *ldb);

INT64 ctrmv_(char *uplo, char *trans, char *diag, INT64 *n, fcomplex *a,
           INT64 *lda, fcomplex *x, INT64 *incx);

INT64 ctrsm_(char *side, char *uplo, char *transa, char *diag, INT64 *m,
           INT64 *n, fcomplex *alpha, fcomplex *a, INT64 *lda, fcomplex *b,
           INT64 *ldb);

INT64 ctrsv_(char *uplo, char *trans, char *diag, INT64 *n, fcomplex *a,
           INT64 *lda, fcomplex *x, INT64 *incx);

INT64 daxpy_(INT64 *n, double *sa, double *sx, INT64 *incx, double *sy,
           INT64 *incy);

INT64 dcopy_(INT64 *n, double *sx, INT64 *incx, double *sy, INT64 *incy);

INT64 dgbmv_(char *trans, INT64 *m, INT64 *n, INT64 *kl, INT64 *ku,
           double *alpha, double *a, INT64 *lda, double *x, INT64 *incx,
           double *beta, double *y, INT64 *incy);

INT64 dgemm_(char *transa, char *transb, INT64 *m, INT64 *n, INT64 *k,
           double *alpha, double *a, INT64 *lda, double *b, INT64 *ldb,
           double *beta, double *c, INT64 *ldc);

INT64 dgemv_(char *trans, INT64 *m, INT64 *n, double *alpha, double *a,
           INT64 *lda, double *x, INT64 *incx, double *beta, double *y, 
           INT64 *incy);

INT64 dger_(INT64 *m, INT64 *n, double *alpha, double *x, INT64 *incx,
          double *y, INT64 *incy, double *a, INT64 *lda);

INT64 drot_(INT64 *n, double *sx, INT64 *incx, double *sy, INT64 *incy,
          double *c, double *s);

INT64 drotg_(double *sa, double *sb, double *c, double *s);

INT64 dsbmv_(char *uplo, INT64 *n, INT64 *k, double *alpha, double *a,
           INT64 *lda, double *x, INT64 *incx, double *beta, double *y, 
           INT64 *incy);

INT64 dscal_(INT64 *n, double *sa, double *sx, INT64 *incx);

INT64 dspmv_(char *uplo, INT64 *n, double *alpha, double *ap, double *x,
           INT64 *incx, double *beta, double *y, INT64 *incy);

INT64 dspr_(char *uplo, INT64 *n, double *alpha, double *x, INT64 *incx,
          double *ap);

INT64 dspr2_(char *uplo, INT64 *n, double *alpha, double *x, INT64 *incx,
           double *y, INT64 *incy, double *ap);

INT64 dswap_(INT64 *n, double *sx, INT64 *incx, double *sy, INT64 *incy);

INT64 dsymm_(char *side, char *uplo, INT64 *m, INT64 *n, double *alpha,
           double *a, INT64 *lda, double *b, INT64 *ldb, double *beta,
           double *c, INT64 *ldc);

INT64 dsymv_(char *uplo, INT64 *n, double *alpha, double *a, INT64 *lda,
           double *x, INT64 *incx, double *beta, double *y, INT64 *incy);

INT64 dsyr_(char *uplo, INT64 *n, double *alpha, double *x, INT64 *incx,
          double *a, INT64 *lda);

INT64 dsyr2_(char *uplo, INT64 *n, double *alpha, double *x, INT64 *incx,
           double *y, INT64 *incy, double *a, INT64 *lda);

INT64 dsyr2k_(char *uplo, char *trans, INT64 *n, INT64 *k, double *alpha,
            double *a, INT64 *lda, double *b, INT64 *ldb, double *beta,
            double *c, INT64 *ldc);

INT64 dsyrk_(char *uplo, char *trans, INT64 *n, INT64 *k, double *alpha,
           double *a, INT64 *lda, double *beta, double *c, INT64 *ldc);

INT64 dtbmv_(char *uplo, char *trans, char *diag, INT64 *n, INT64 *k,
           double *a, INT64 *lda, double *x, INT64 *incx);

INT64 dtbsv_(char *uplo, char *trans, char *diag, INT64 *n, INT64 *k,
           double *a, INT64 *lda, double *x, INT64 *incx);

INT64 dtpmv_(char *uplo, char *trans, char *diag, INT64 *n, double *ap,
           double *x, INT64 *incx);

INT64 dtpsv_(char *uplo, char *trans, char *diag, INT64 *n, double *ap,
           double *x, INT64 *incx);

INT64 dtrmm_(char *side, char *uplo, char *transa, char *diag, INT64 *m,
           INT64 *n, double *alpha, double *a, INT64 *lda, double *b, 
           INT64 *ldb);

INT64 dtrmv_(char *uplo, char *trans, char *diag, INT64 *n, double *a,
           INT64 *lda, double *x, INT64 *incx);

INT64 dtrsm_(char *side, char *uplo, char *transa, char *diag, INT64 *m,
           INT64 *n, double *alpha, double *a, INT64 *lda, double *b, 
           INT64 *ldb);

INT64 dtrsv_(char *uplo, char *trans, char *diag, INT64 *n, double *a,
           INT64 *lda, double *x, INT64 *incx);


INT64 saxpy_(INT64 *n, float *sa, float *sx, INT64 *incx, float *sy, INT64 *incy);

INT64 scopy_(INT64 *n, float *sx, INT64 *incx, float *sy, INT64 *incy);

INT64 sgbmv_(char *trans, INT64 *m, INT64 *n, INT64 *kl, INT64 *ku,
           float *alpha, float *a, INT64 *lda, float *x, INT64 *incx,
           float *beta, float *y, INT64 *incy);

INT64 sgemm_(char *transa, char *transb, INT64 *m, INT64 *n, INT64 *k,
           float *alpha, float *a, INT64 *lda, float *b, INT64 *ldb,
           float *beta, float *c, INT64 *ldc);

INT64 sgemv_(char *trans, INT64 *m, INT64 *n, float *alpha, float *a,
           INT64 *lda, float *x, INT64 *incx, float *beta, float *y, 
           INT64 *incy);

INT64 sger_(INT64 *m, INT64 *n, float *alpha, float *x, INT64 *incx,
          float *y, INT64 *incy, float *a, INT64 *lda);

INT64 srot_(INT64 *n, float *sx, INT64 *incx, float *sy, INT64 *incy,
          float *c, float *s);

INT64 srotg_(float *sa, float *sb, float *c, float *s);

INT64 ssbmv_(char *uplo, INT64 *n, INT64 *k, float *alpha, float *a,
           INT64 *lda, float *x, INT64 *incx, float *beta, float *y, 
           INT64 *incy);

INT64 sscal_(INT64 *n, float *sa, float *sx, INT64 *incx);

INT64 sspmv_(char *uplo, INT64 *n, float *alpha, float *ap, float *x,
           INT64 *incx, float *beta, float *y, INT64 *incy);

INT64 sspr_(char *uplo, INT64 *n, float *alpha, float *x, INT64 *incx,
          float *ap);

INT64 sspr2_(char *uplo, INT64 *n, float *alpha, float *x, INT64 *incx,
           float *y, INT64 *incy, float *ap);

INT64 sswap_(INT64 *n, float *sx, INT64 *incx, float *sy, INT64 *incy);

INT64 ssymm_(char *side, char *uplo, INT64 *m, INT64 *n, float *alpha,
           float *a, INT64 *lda, float *b, INT64 *ldb, float *beta,
           float *c, INT64 *ldc);

INT64 ssymv_(char *uplo, INT64 *n, float *alpha, float *a, INT64 *lda,
           float *x, INT64 *incx, float *beta, float *y, INT64 *incy);

INT64 ssyr_(char *uplo, INT64 *n, float *alpha, float *x, INT64 *incx,
          float *a, INT64 *lda);

INT64 ssyr2_(char *uplo, INT64 *n, float *alpha, float *x, INT64 *incx,
           float *y, INT64 *incy, float *a, INT64 *lda);

INT64 ssyr2k_(char *uplo, char *trans, INT64 *n, INT64 *k, float *alpha,
            float *a, INT64 *lda, float *b, INT64 *ldb, float *beta,
            float *c, INT64 *ldc);

INT64 ssyrk_(char *uplo, char *trans, INT64 *n, INT64 *k, float *alpha,
           float *a, INT64 *lda, float *beta, float *c, INT64 *ldc);

INT64 stbmv_(char *uplo, char *trans, char *diag, INT64 *n, INT64 *k,
           float *a, INT64 *lda, float *x, INT64 *incx);

INT64 stbsv_(char *uplo, char *trans, char *diag, INT64 *n, INT64 *k,
           float *a, INT64 *lda, float *x, INT64 *incx);

INT64 stpmv_(char *uplo, char *trans, char *diag, INT64 *n, float *ap,
           float *x, INT64 *incx);

INT64 stpsv_(char *uplo, char *trans, char *diag, INT64 *n, float *ap,
           float *x, INT64 *incx);

INT64 strmm_(char *side, char *uplo, char *transa, char *diag, INT64 *m,
           INT64 *n, float *alpha, float *a, INT64 *lda, float *b, 
           INT64 *ldb);

INT64 strmv_(char *uplo, char *trans, char *diag, INT64 *n, float *a,
           INT64 *lda, float *x, INT64 *incx);

INT64 strsm_(char *side, char *uplo, char *transa, char *diag, INT64 *m,
           INT64 *n, float *alpha, float *a, INT64 *lda, float *b, 
           INT64 *ldb);

INT64 strsv_(char *uplo, char *trans, char *diag, INT64 *n, float *a,
           INT64 *lda, float *x, INT64 *incx);

INT64 zaxpy_(INT64 *n, dcomplex *ca, dcomplex *cx, INT64 *incx, dcomplex *cy,
           INT64 *incy);

INT64 zcopy_(INT64 *n, dcomplex *cx, INT64 *incx, dcomplex *cy, INT64 *incy);

INT64 zdscal_(INT64 *n, double *sa, dcomplex *cx, INT64 *incx);

INT64 zgbmv_(char *trans, INT64 *m, INT64 *n, INT64 *kl, INT64 *ku,
           dcomplex *alpha, dcomplex *a, INT64 *lda, dcomplex *x, INT64 *incx,
           dcomplex *beta, dcomplex *y, INT64 *incy);

INT64 zgemm_(char *transa, char *transb, INT64 *m, INT64 *n, INT64 *k,
           dcomplex *alpha, dcomplex *a, INT64 *lda, dcomplex *b, INT64 *ldb,
           dcomplex *beta, dcomplex *c, INT64 *ldc);

INT64 zgemv_(char *trans, INT64 *m, INT64 *n, dcomplex *alpha, dcomplex *a,
           INT64 *lda, dcomplex *x, INT64 *incx, dcomplex *beta, dcomplex *y,
           INT64 *incy);

INT64 zgerc_(INT64 *m, INT64 *n, dcomplex *alpha, dcomplex *x, INT64 *incx,
           dcomplex *y, INT64 *incy, dcomplex *a, INT64 *lda);

INT64 zgeru_(INT64 *m, INT64 *n, dcomplex *alpha, dcomplex *x, INT64 *incx,
           dcomplex *y, INT64 *incy, dcomplex *a, INT64 *lda);

INT64 zhbmv_(char *uplo, INT64 *n, INT64 *k, dcomplex *alpha, dcomplex *a,
           INT64 *lda, dcomplex *x, INT64 *incx, dcomplex *beta, dcomplex *y,
           INT64 *incy);

INT64 zhemm_(char *side, char *uplo, INT64 *m, INT64 *n, dcomplex *alpha,
           dcomplex *a, INT64 *lda, dcomplex *b, INT64 *ldb, dcomplex *beta,
           dcomplex *c, INT64 *ldc);

INT64 zhemv_(char *uplo, INT64 *n, dcomplex *alpha, dcomplex *a, INT64 *lda,
           dcomplex *x, INT64 *incx, dcomplex *beta, dcomplex *y, INT64 *incy);

INT64 zher_(char *uplo, INT64 *n, double *alpha, dcomplex *x, INT64 *incx,
          dcomplex *a, INT64 *lda);

INT64 zher2_(char *uplo, INT64 *n, dcomplex *alpha, dcomplex *x, INT64 *incx,
           dcomplex *y, INT64 *incy, dcomplex *a, INT64 *lda);

INT64 zher2k_(char *uplo, char *trans, INT64 *n, INT64 *k, dcomplex *alpha,
            dcomplex *a, INT64 *lda, dcomplex *b, INT64 *ldb, double *beta,
            dcomplex *c, INT64 *ldc);

INT64 zherk_(char *uplo, char *trans, INT64 *n, INT64 *k, double *alpha,
           dcomplex *a, INT64 *lda, double *beta, dcomplex *c, INT64 *ldc);

INT64 zhpmv_(char *uplo, INT64 *n, dcomplex *alpha, dcomplex *ap, dcomplex *x,
           INT64 *incx, dcomplex *beta, dcomplex *y, INT64 *incy);

INT64 zhpr_(char *uplo, INT64 *n, double *alpha, dcomplex *x, INT64 *incx,
          dcomplex *ap);

INT64 zhpr2_(char *uplo, INT64 *n, dcomplex *alpha, dcomplex *x, INT64 *incx,
           dcomplex *y, INT64 *incy, dcomplex *ap);

INT64 zrotg_(dcomplex *ca, dcomplex *cb, double *c, dcomplex *s);

INT64 zscal_(INT64 *n, dcomplex *ca, dcomplex *cx, INT64 *incx);

INT64 zswap_(INT64 *n, dcomplex *cx, INT64 *incx, dcomplex *cy, INT64 *incy);

INT64 zsymm_(char *side, char *uplo, INT64 *m, INT64 *n, dcomplex *alpha,
           dcomplex *a, INT64 *lda, dcomplex *b, INT64 *ldb, dcomplex *beta,
           dcomplex *c, INT64 *ldc);

INT64 zsyr2k_(char *uplo, char *trans, INT64 *n, INT64 *k, dcomplex *alpha,
            dcomplex *a, INT64 *lda, dcomplex *b, INT64 *ldb, dcomplex *beta,
            dcomplex *c, INT64 *ldc);

INT64 zsyrk_(char *uplo, char *trans, INT64 *n, INT64 *k, dcomplex *alpha,
           dcomplex *a, INT64 *lda, dcomplex *beta, dcomplex *c, INT64 *ldc);

INT64 ztbmv_(char *uplo, char *trans, char *diag, INT64 *n, INT64 *k,
           dcomplex *a, INT64 *lda, dcomplex *x, INT64 *incx);

INT64 ztbsv_(char *uplo, char *trans, char *diag, INT64 *n, INT64 *k,
           dcomplex *a, INT64 *lda, dcomplex *x, INT64 *incx);

INT64 ztpmv_(char *uplo, char *trans, char *diag, INT64 *n, dcomplex *ap,
           dcomplex *x, INT64 *incx);

INT64 ztpsv_(char *uplo, char *trans, char *diag, INT64 *n, dcomplex *ap,
           dcomplex *x, INT64 *incx);

INT64 ztrmm_(char *side, char *uplo, char *transa, char *diag, INT64 *m,
           INT64 *n, dcomplex *alpha, dcomplex *a, INT64 *lda, dcomplex *b,
           INT64 *ldb);

INT64 ztrmv_(char *uplo, char *trans, char *diag, INT64 *n, dcomplex *a,
           INT64 *lda, dcomplex *x, INT64 *incx);

INT64 ztrsm_(char *side, char *uplo, char *transa, char *diag, INT64 *m,
           INT64 *n, dcomplex *alpha, dcomplex *a, INT64 *lda, dcomplex *b,
           INT64 *ldb);

INT64 ztrsv_(char *uplo, char *trans, char *diag, INT64 *n, dcomplex *a,
           INT64 *lda, dcomplex *x, INT64 *incx);
