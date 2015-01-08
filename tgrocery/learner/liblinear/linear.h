#include <stdint.h>

#ifndef _LIBLINEAR_H
#define _LIBLINEAR_H
#ifndef INT64_DEFINED
typedef int64_t INT64;
#define INT64_DEFINED
#endif

#ifdef __cplusplus
extern "C" {
#endif

struct feature_node
{
	INT64 index;
	double value;
};

struct problem
{
	INT64 l, n;
	double *y;
	struct feature_node **x;
	double bias;            /* < 0 if no bias term */  
};

enum { L2R_LR, L2R_L2LOSS_SVC_DUAL, L2R_L2LOSS_SVC, L2R_L1LOSS_SVC_DUAL, MCSVM_CS, L1R_L2LOSS_SVC, L1R_LR, L2R_LR_DUAL, L2R_L2LOSS_SVR = 11, L2R_L2LOSS_SVR_DUAL, L2R_L1LOSS_SVR_DUAL }; /* solver_type */

struct parameter
{
	INT64 solver_type;

	/* these are for training only */
	double eps;	        /* stopping criteria */
	double C;
	INT64 nr_weight;
	INT64 *weight_label;
	double* weight;
	double p;
};

struct model
{
	struct parameter param;
	INT64 nr_class;		/* number of classes */
	INT64 nr_feature;
	double *w;
	INT64 *label;		/* label of each class */
	double bias;
};

struct model* train(const struct problem *prob, const struct parameter *param);
void cross_validation(const struct problem *prob, const struct parameter *param, INT64 nr_fold, double *target);

double predict_values(const struct model *model_, const struct feature_node *x, double* dec_values);
double predict(const struct model *model_, const struct feature_node *x);
double predict_probability(const struct model *model_, const struct feature_node *x, double* prob_estimates);

INT64 save_model(const char *model_file_name, const struct model *model_);
struct model *load_model(const char *model_file_name);

INT64 get_nr_feature(const struct model *model_);
INT64 get_nr_class(const struct model *model_);
void get_labels(const struct model *model_, INT64* label);

void free_model_content(struct model *model_ptr);
void free_and_destroy_model(struct model **model_ptr_ptr);
void destroy_param(struct parameter *param);

const char *check_parameter(const struct problem *prob, const struct parameter *param);
INT64 check_probability_model(const struct model *model);
void set_print_string_function(void (*print_func) (const char*));

#ifdef __cplusplus
}
#endif

#endif /* _LIBLINEAR_H */

