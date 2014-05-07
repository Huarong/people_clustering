# Web People Search

### Task Source

Task Description:
http://nlp.uned.es/weps/weps-2/weps2-task-guidelines
Training Data:
http://nlp.uned.es/weps/weps-1/weps1-data
Test Data:
http://nlp.uned.es/weps/weps-2/weps2-data


### How to Use

There are 12 processing steps in the program. Every step will save its results in the directory `pickle`. The disadvantage of this is that when we modify and run again some steps, we don't need rerun the former steps, which will save a bunch of time.

The 12 processing steps are listed as follows:

    processes_dict = {
        1: self.run_map_doc_id,
        2: self.run_text_extraction,
        3: self.run_feature_extractor,
        4: self.run_extra_feature_extractor,
        5: self.run_feature_filter,
        6: self.run_feature_vector,
        7: self.run_svd,
        8: self.run_consine,
        9: self.run_cluster,
        10: self.run_gen_result,
        11: self.run_map_back,
        12: self.run_eval
    }

Another import component to run the program is the configure file. Since we will try combinations of different method and parameters, the configure file helps us to run the program as we want. Just modify or create another configure and run with it. The configure files are JSON format files located in the directory `configure`.

The configure file looks like this:

    {
        "version": "2008test",
        "cluster_method": "louvain",
        "log_path": "log/2008test.louvain.NN.log",
        "webpages_dir": "data/weps-2/data/test/web_pages",
        "mapped_webpages_dir": "pickle/2008test/mapped_webpages_dir/",
        "id_mapper_pickle_dir": "pickle/2008test/id_mapper/",
        "metadata_dir": "data/weps-2/data/test/metadata/",
        "body_text_dir": "pickle/2008test/bodytext/",
        "feature_dir": "pickle/2008test/features/",
        "selected_POS": ["NN"],
        "feature_threshold": 500,
        "selected_feature_dir": "pickle/2008test/NN_features/",
        "matrix_dir": "pickle/2008test/matrix_NN/word/",
        "is_svd": false,
        "svd_matrix_dir": "pickle/2008test/svd_matrix_NN/",
        "similarity_method": "jaccard",
        "cosine_dir": "pickle/2008test/cosine_NN/",
        "category_dir": "pickle/2008test/category/louvain_NN",
        "before_map_back_result_dir": "pickle/2008test/before_map_back_result/louvain_NN",
        "result_dir": "pickle/2008test/result/louvain_NN_jaccard",
        "result_file_extension": "xml"
    }

So the command line of running the program is:

    usage: exe.py [-h] [-b BEGIN] [-e END] configure
    Execute a people clustering task

    positional arguments:
      configure             The config path

    optional arguments:
      -h, --help            show this help message and exit
      -b BEGIN, --begin BEGIN
                            The process step to begin
      -e END, --end END     The process step to end


For example:

    python people_clustering/exe.py configure/2008test.NN.nltk.json -b 8 -e 12

