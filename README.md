# Classification of Error-related Potential (ErrP) from EEG signals

## Objective
In this mini project, you must develop an offline BCI classifier for detection of Error-related Potentials (ErrPs) from EEG signals. You will use a publicly available dataset that we have selected for this project, however, your approach to data preprocessing, feature extraction, and model selection is entirely flexible and up to you.
Dataset

You must use the ErrP dataset shared by Chavarriaga and Millán (2010) [1]. The data is accessible via the following link under title “22. Monitoring error-related potentials (013-2015)”:
https://bnci-horizon-2020.eu/database/data-sets

This dataset was collected during an experiment designed to elicit error-related potentials when human users (n = 6) monitored the behavior of an external agent [1]. The agent made decisions (correct or incorrect) in each trial over which users had no control. EEG recordings were collected from each subject in two sessions separated by several weeks.
You can find a full description of the study design and the data files in [1] and the document “data description”. Both documents are provided in the supplementary material.

## Implementation
The primary goal is for you 
1. to design and implement a pipeline for classifying ErrPs from the EEG data 
1. to present and interpret the classification results.

Within this framework, you are free to define your specific research question. For instance, you might choose to use the entire dataset for a mixed-subject analysis or focus on cross-subject or cross-session classification. This choice is up to you.

You may also use any programming language or ML framework that suits your approach. For feature extraction, various methods are available (see [2] for a comparative overview, article provided in supplementary materials). Again, you are free to select whichever method best fits your research question.
Requirements

For this mind project, you must deliver two deliverables: a written report (max 2 pages excluding references) and a presentation (10 minutes) during the second interview.

1. Written Report (deadline July 4th)
    * Submit a concise 2-page report (excluding references) in PDF format.
    * The report should include only the Methods and Results sections:
        - Describe your signal processing, feature engineering, and model training pipeline.
        - Present relevant performance metrics such as accuracy, F1-score, etc.
        - Visualizations of results are highly encouraged.
        - You can include a link to your code/GitHub repository in the report, but this is entirely optional.
1. Presentation (will be scheduled after July 4)
    - Prepare a 10-minute presentation summarizing your motivation, approach, results and a short discussion.
    - You will deliver this during the second interview that will be scheduled after July 4th. After the presentation, we will have a Q&A session for general or project-related questions. In this session, you can also ask any questions you have for us. 

## Evaluation Criteria
Your report and presentation will be assessed based on the following aspects:

- Soundness and creativity of your approach
- Clarity and completeness of your report
- Quality and insightfulness of your analysis and visualizations
- Presentation skills and your ability to explain technical decisions


## Submission Details

- Report submission deadline: July 4 
- Submission format: PDF report 
- Email to: both Maryam and Herke.

 
## References:
[1] Chavarriaga, R., & Millán, J. D. R. (2010). Learning from EEG error-related potentials in noninvasive brain-computer interfaces. IEEE Transactions on Neural Systems and Rehabilitation Engineering, 18(4), 381-388.

[2] Yasemin, M., Cruz, A., Nunes, U. J., & Pires, G. (2023). Single trial detection of error-related potentials in brain–machine interfaces: a survey and comparison of methods. Journal of Neural Engineering, 20(1), 016015.