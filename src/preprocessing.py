#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from tqdm import tqdm
from loguru import logger

from src.config import AGGREGATE_COLUMNS
from src.paths import RAW_DATASET_PATH, FINAL_DATASET_PATH


def check_one2one_mapping(df, id_col, value_col):
    filter_df = df[[id_col, value_col]].drop_duplicates()
    assert len(np.unique(filter_df[id_col].values)) == len(filter_df[value_col].values)


def replace_mapping(df, id_col, value_col, mapper):
    for key, value in mapper.items():
        df.loc[df[id_col] == key, value_col] = value
    return df


def main():
    df = pd.read_csv(RAW_DATASET_PATH)
    logger.info("Dataset {} loaded. Shape : {}".format(RAW_DATASET_PATH, df.shape))

    df = df.dropna()
    logger.info("Dataset with NA deleted. Shape : {}".format(df.shape))

    df.columns = [x.strip() for x in df.columns]
    df = replace_mapping(df, "UnitTypeID", "UnitType", {92: "BUILDING-WIDE", 24: "PUBLIC PARTS", 93: "PUBLIC AREA"})
    df = replace_mapping(
        df,
        "CodeID",
        "Code",
        {658: "NO SUPPLY TO ENTIRE BUILDING", 1389: "COLLAPSING OR FALLING", 649: "NO WATER SUPPLY TO ENTIRE BUILDING"},
    )
    logger.info("Data Cleanup has been completed successfully")

    check_one2one_mapping(df, "ProblemID", "ComplaintID")
    check_one2one_mapping(df, "UnitTypeID", "UnitType")
    check_one2one_mapping(df, "SpaceTypeID", "SpaceType")
    check_one2one_mapping(df, "TypeID", "Type")
    check_one2one_mapping(df, "MajorCategoryID", "MajorCategory")
    check_one2one_mapping(df, "MinorCategoryID", "MinorCategory")
    check_one2one_mapping(df, "CodeID", "Code")
    check_one2one_mapping(df, "StatusID", "Status")
    logger.info("All Data ID and Descriptions are consistent")

    result_df = df[
        ["ProblemID", "ComplaintID", "UnitType", "SpaceType", "MajorCategory", "MinorCategory", "Code"]
    ].copy()
    assert len(AGGREGATE_COLUMNS) >= 1
    result_df["Entity"] = result_df[AGGREGATE_COLUMNS[0]]
    for agg_column in AGGREGATE_COLUMNS[1:]:
        result_df["Entity"] = result_df["Entity"] + " | " + result_df[agg_column]
    logger.info("Entity used : {}".format(AGGREGATE_COLUMNS))

    with open(FINAL_DATASET_PATH, "w+") as f:
        for group_id, group_df in tqdm(result_df.groupby("ComplaintID")):
            try:
                x = sorted(list(set(group_df["Entity"].values.tolist())))
            except:
                print(group_df["Entity"].values.tolist())
                raise ValueError
            f.write(",".join(x))
            f.write("\n")
    logger.info("Data successfully written to : {}".format(FINAL_DATASET_PATH))


if __name__ == "__main__":
    main()
