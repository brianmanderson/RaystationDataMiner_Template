from AbstractInfoStructure.EvaluationTools import *


def find_all_rois(header_databases: PatientHeaderDatabases):
    """
    :param header_databases:
    :return:
    """
    all_rois = []
    for header_database in header_databases.HeaderDatabases.values():
        for pat in header_database.PatientHeaders.values():
            for case in pat.Cases:
                for roi in case.ROIS:
                    if roi.Name.lower() not in all_rois:
                        all_rois.append(roi.Name.lower())
    reduced_all_rois = [i for i in all_rois if i.find('ptv') == -1 and i.find('0') == -1 and i.find('1') == -1 and
                        i.find('opt') == -1 and i.find('2') == -1 and i.find('3') == -1 and i.find('hot') == -1 and
                        i.find('cold') == -1 and i.find('avo') == -1 and i.find('norm') == -1 and i.find('tune') == -1
                        and i.find('5') == -1 and len(i) > 2 and i.find('ring') == -1 and i.find('couch') == -1
                        and i.find('arti') == -1 and i.find('max') == -1 and i.find('min') == -1 and i.find('4') == -1
                        and i.find('push') == -1 and i.find('shell') == -1 and i.find('warm') == -1 and
                        i.find('avd') == -1]
    return reduced_all_rois


def main():
    network_path = r'\\vscifs1\PhysicsQAdata\BMA\RayStationDataStructure\DataBases'
    local_db_path = r'C:\Users\u376045\Modular_Projects\Local_Databases'
    if not os.path.exists(local_db_path) and os.path.exists(r'C:\Users\Markb\Modular_Projects'):
        local_db_path = r'C:\Users\Markb\Modular_Projects\Local_Databases'
    # TODO Change local_db_path to be where you would like to save the data!

    MRNs = None
    """
    If we have a list of MRNs that we want specifically, we can add them
    """
    if os.path.exists(network_path):
        update_database(network_path, local_db_path)

    """
    Lets first load up just the basic information from all patients in our databases
    """
    header_databases: PatientHeaderDatabases
    header_databases = PatientHeaderDatabases()
    header_databases.build_from_folder(local_db_path, specific_mrns=MRNs, tqdm=tqdm)

    header_databases.delete_unapproved_patients()
    all_rois = find_all_rois(header_databases)

    wanted_type = ['organ']
    header_databases = identify_wanted_headers(header_databases, wanted_roi_list=['parotid_r'],
                                               wanted_type=wanted_type)
    """
    Now we load the entirety of patient data
    """
    databases = header_databases.return_patient_databases(tqdm)
    databases.delete_unapproved_patients()

    mrns = []
    """
    Why do we do this? Because a patient could exist across multiple databases!
    Take the most RECENT one, and move on
    """
    db_list = ['10ASP1', 'Deceased', '2023', '2022', '2021', '2020', '2019', '2018',
               '2017', '2016']
    for db_name in db_list:
        db = databases.Databases[db_name]
        for patient in db.Patients.values():
            if patient.MRN in mrns:
                continue
            mrns.append(patient.MRN)
            for case in patient.Cases:
                for plan in case.TreatmentPlans:
                    if plan.Review is not None:
                        review: ReviewClass
                        review = plan.Review
                        if review.ApprovalStatus == 'Approved':
                            exams = [e for e in case.Examinations if e.ExamName == plan.Referenced_Exam_Name]
                            for exam in exams:
                                for roi in exam.ROIs:
                                    print(roi.Name)


if __name__ == '__main__':
    main()
