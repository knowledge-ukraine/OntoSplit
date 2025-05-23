# -*- coding: utf8 -*-

import os
import json
import copy
import time
from threading import Thread, Lock, stack_size
import traceback

from SPARQLWrapper import SPARQLWrapper, JSON

stack_size(512*1024)

class QueryExec:
    def __init__(self, jena_endpoint="http://localhost:3030/", user="", password="", ontologies=None):
        self.jena_endpoint = jena_endpoint
        self.ontologies = ontologies
        self.user = user
        self.password = password

    def execute_query(self, query, ontology):
        ontology_object = SPARQLWrapper(self.jena_endpoint + ontology)
        ontology_object.setCredentials(self.user, self.password)
        ontology_object.setReturnFormat(JSON)
        ontology_object.setQuery(query)
        return ontology_object.query().convert()

    @staticmethod
    def form_answer(query_results, output_instruction):
        def make_structure(initial, out, prim):
            field_found = False
            found_items = list()
            for f in initial:
                if f != prim:
                    for item in initial[f]:
                        if "rel_field" in item:
                            if item["rel_field"] in out:
                                field_found = True
                                found_items.append(f)
                                for struct in out[item["rel_field"]]:
                                    if "value" in struct and struct["value"] == item["rel"]:
                                        if f not in struct:
                                            # Checking if the parent is correct
                                            if item.get("parent", "") == struct.get("rel", ""):
                                                struct[f] = [copy.deepcopy(item)]
                                        else:
                                            # Checking if items are siblings
                                            if item.get("parent", "") == struct[f][0].get("parent", ""):
                                                add = True
                                                for i in struct[f]:
                                                    if i.get("value", "") == item.get("value", "") and i.get("value", "") != "":
                                                        add = False
                                                        break
                                                if add:
                                                    struct[f].append(copy.deepcopy(item))
                                    elif "values" in struct and item["rel"] in struct["values"]:
                                        if isinstance(struct["values"], list):
                                            values_dict = dict()
                                            for val in struct["values"]:
                                                values_dict[val] = dict()
                                            struct["values"] = copy.deepcopy(values_dict)
                                        if isinstance(struct["values"], dict):
                                            if f not in struct["values"][item["rel"]]:
                                                struct["values"][item["rel"]][f] = [copy.deepcopy(item)]
                                            else:
                                                do_add = True
                                                for i in struct["values"][item["rel"]][f]:
                                                    chech_val_1 = i.get("value")
                                                    chech_val_2 = item.get("value")
                                                    if str(chech_val_1).lower().strip() == str(chech_val_2).lower().strip():
                                                        do_add = False
                                                        break
                                                if do_add:
                                                    struct["values"][item["rel"]][f].append(copy.deepcopy(item))

            if field_found and len(found_items) > 0:
                for f_2 in out:
                    if isinstance(out[f_2], list) and f_2 not in ["verbose", "rel", "rel_field", "value"]:
                        for i_2 in out[f_2]:
                            if isinstance(i_2, dict):
                                make_structure(initial, i_2, f_2)

        s_time = time.time()
        current_field_id = 1
        output = dict()
        primary = None
        for row in query_results:
            for field in row:
                if isinstance(output_instruction[field].get("sortage"), str):
                    if field not in output:
                        primary = field
                        output[field] = [{"value": row[field].get("value"),
                                         "verbose": output_instruction[field].get("verbose"),
                                          "id": current_field_id}]
                        current_field_id += 1
                    else:
                        value = row[field].get("value")
                        to_add = True
                        for v in output[field]:
                            if v["value"] == value:
                                to_add = False
                                break
                        if to_add:
                            output[field].append({"value": value,
                                                  "verbose": output_instruction[field].get("verbose"),
                                                  "id": current_field_id})
                            current_field_id += 1
                elif isinstance(output_instruction[field].get("sortage"), dict):
                    by_each = output_instruction[field]["sortage"].get("by each")
                    group = output_instruction[field]["sortage"].get("group")
                    if isinstance(by_each, str) and by_each in row:
                        if field not in output:
                            parent = output_instruction[by_each].get("sortage")
                            if isinstance(parent, dict):
                                parent = parent.get("by each", parent.get("group"))
                            output[field] = [{"value": row[field].get("value"),
                                              "rel": row[by_each].get("value"),
                                              "rel_field": by_each,
                                              "verbose": output_instruction[field].get("verbose"),
                                              "id": current_field_id,
                                              "parent": row.get(parent, {}).get("value", "")}]
                            current_field_id += 1
                        else:
                            value = row[field].get("value")
                            rel = row[by_each].get("value")
                            to_add = True
                            for v in output[field]:
                                if v["value"] == value and v["rel"] == rel:
                                    to_add = False
                                    break
                            if to_add:
                                parent = output_instruction[by_each].get("sortage")
                                if isinstance(parent, dict):
                                    parent = parent.get("by each", parent.get("group"))
                                output[field].append({"value": row[field].get("value"),
                                                      "rel": row[by_each].get("value"),
                                                      "rel_field": by_each,
                                                      "verbose": output_instruction[field].get("verbose"),
                                                      "id": current_field_id,
                                                      "parent": row.get(parent, {}).get("value", "")})
                                current_field_id += 1
                    if isinstance(group, str) and group in row:
                        if field not in output:
                            parent = output_instruction[group].get("sortage")
                            if isinstance(parent, dict):
                                parent = parent.get("by each", parent.get("group"))
                            output[field] = [{"values": [row[field].get("value")],
                                              "rel": row[group].get("value"),
                                              "rel_field": group,
                                              "verbose": output_instruction[field].get("verbose"),
                                              "id": current_field_id,
                                              "parent": row.get(parent, {}).get("value", "")}]
                            current_field_id += 1
                        else:
                            value = row[field].get("value")
                            rel = row[group].get("value")
                            new_item = True
                            for v in output[field]:
                                if v["rel"] == rel and value not in v["values"]:
                                    v["values"].append(value)
                                    new_item = False
                                    break
                                if v["rel"] == rel and value in v["values"]:
                                    new_item = False
                                    break
                            if new_item:
                                parent = output_instruction[group].get("sortage")
                                if isinstance(parent, dict):
                                    parent = parent.get("by each", parent.get("group"))
                                output[field].append({"values": [row[field].get("value")],
                                                      "rel": row[group].get("value"),
                                                      "rel_field": group,
                                                      "verbose": output_instruction[field].get("verbose"),
                                                      "id": current_field_id,
                                                      "parent": row.get(parent, {}).get("value", "")})
                                current_field_id += 1

        if primary is not None:
            output_tmp = {primary: copy.deepcopy(output[primary])}
            make_structure(output, output_tmp, primary)
            output = output_tmp
        else:
            return {}
        return output

    def process_query_set(self, query_set):
        output = dict()
        for sem_type in query_set:
            print(query_set[sem_type])
            print()
            for query_struct in query_set[sem_type]:
                print(query_struct)
                query = query_struct.get('query')
                instr = query_struct.get('outputs')
                out_data = list()
                if query is not None and instr is not None:
                    pr_pool = [Thread(target=self.multiontology_query, name=ontology, args=[query, ontology, out_data])
                               for ontology in self.ontologies]
                    for proc in pr_pool:
                        proc.start()
                    for proc in pr_pool:
                        proc.join()
                    too_long = False
                    if sem_type == "contexts" and len(out_data) > 100:
                        too_long = True
                    elif len(out_data) > 150:
                        too_long = True
                    response = self.form_answer(out_data, instr)
                    if sem_type not in output:
                        output[sem_type] = [{
                            "response": copy.deepcopy(response),
                            "input": query_struct.get('input'),
                            "too_long": too_long
                        }]
                    else:
                        output[sem_type].append({
                            "response": copy.deepcopy(response),
                            "input": query_struct.get('input'),
                            "too_long": too_long
                        })
        return output

    def multiontology_query(self, query, ont_name, out_data):
        s_time = time.time()
        current_result = self.execute_query(query, ont_name)
        if ('results' in current_result and 'bindings' in current_result['results'] and
                len(current_result['results']['bindings']) > 0):
            lock = Lock()
            lock.acquire()
            out_data += current_result['results']['bindings']
            lock.release()
        print(time.time() - s_time)

    def single_query(self, query, ont_name):
        s_time = time.time()
        current_result = self.execute_query(query, ont_name)
        print(time.time() - s_time)
        return current_result['results']['bindings']

    def test_quering(self, query):
        s_time = time.time()
        out_data = list()
        if query is not None:
            pr_pool = [Thread(target=self.multiontology_query, name=ontology, args=[query, ontology, out_data])
                       for ontology in self.ontologies]
            for proc in pr_pool:
                proc.start()
            for proc in pr_pool:
                proc.join()
        ex_time = time.time() - s_time
        return out_data, ex_time

    def test_quering_seq(self, query, ont_n=None):
        s_time = time.time()
        out_data = list()
        if query is not None and len(self.ontologies) > 0:
            if ont_n is None:
                for ontology in self.ontologies:
                    out_data += self.single_query(query, ontology)
            else:
                for ontology in self.ontologies[ont_n]:
                    out_data += self.single_query(query, ontology)

        ex_time = time.time() - s_time
        return out_data, ex_time


if __name__ == "__main__":
    ontology_settings_file = "ontology_settings.json"
    ontology_settings = json.loads(open(ontology_settings_file, "r", encoding="utf-8").read())
    queries_repeating = int(ontology_settings["queries_repeating"])
    test_queries = [q.strip() for q in open("test_queries.txt", "r").read().split("__|__")]
    query_exec = QueryExec(jena_endpoint=ontology_settings["jena_endpoint"],
                           user=ontology_settings["jena_user"],
                           password=ontology_settings["jena_password"],
                           ontologies=ontology_settings["ontologies"])
    results = dict()
    if len(ontology_settings["ontologies"]) > 0:
        if isinstance(ontology_settings["ontologies"], str):
            for n_q, query in enumerate(test_queries):
                times_for_query = list()
                res = ""
                for i in range(queries_repeating):
                    if ontology_settings["parallel"]:
                        res, t = query_exec.test_quering(query)
                    else:
                        res, t = query_exec.test_quering_seq(query)
                    times_for_query.append(t)
                results[str(n_q)] = {
                    "times": times_for_query,
                    "av_time": sum(times_for_query)/float(len(times_for_query)),
                    "min_time": min(times_for_query),
                    "max_time": max(times_for_query),
                    "results_length": len(res)
                }
                print(n_q, sum(times_for_query)/float(len(times_for_query)))
            avg_time = sum([results[q_num]["av_time"] for q_num in results]) / float(len(results))
            avg_min_time = sum([results[q_num]["min_time"] for q_num in results]) / float(len(results))
            avg_max_time = sum([results[q_num]["max_time"] for q_num in results]) / float(len(results))
            results["avg_time"] = avg_time
            results["avg_min_time"] = avg_min_time
            results["avg_max_time"] = avg_max_time
        else:
            for n, ont in enumerate(ontology_settings["ontologies"]):
                for n_q, query in enumerate(test_queries):
                    times_for_query = list()
                    res = ""
                    for i in range(queries_repeating):
                        if ontology_settings["parallel"]:
                            res, t = query_exec.test_quering(query)
                        else:
                            res, t = query_exec.test_quering_seq(query, ont_n=n)
                        times_for_query.append(t)
                    results[str(n_q) + "_" + str(n)] = {
                        "times": times_for_query,
                        "av_time": sum(times_for_query) / float(len(times_for_query)),
                        "min_time": min(times_for_query),
                        "max_time": max(times_for_query),
                        "results_length": len(res)
                    }
                    print(n_q, sum(times_for_query) / float(len(times_for_query)))
        print(results)
        out_f = open("results.json", "w")
        out_f.write(json.dumps(results, indent=2))
        out_f.close()





