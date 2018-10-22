from Porter import FeatureCombiner, Porter

feature_combiners = list()
feature_combiners.append(FeatureCombiner(brand="handuyishe", class_=u"T恤"))
feature_combiners.append(FeatureCombiner(brand="hm", class_=u"衬衫"))
feature_combiners.append(FeatureCombiner(brand="zara", class_=u"上衣"))

porter = Porter(model_path=r"D:\python_project\TmallSpider\classification_network\models\2018-10-21\4.pkl")
porter.file_picker(target_dir=r"E:\tamll_picked", feature_combiners=feature_combiners, labels=["领型", ])
