#!/bin/bash

mkdir -p project-root/{processes/{extract_variables,generate_velocity,validate_schema,export_task},site/{views,templates},examples/{mzov,sch_lkuv,signatures},archive/{2023_legacy,2024_archive},tests/fixtures,shared,docs}

touch project-root/README.md
touch project-root/processes/extract_variables/{extract_variables_from_export_df.py,README.md}
touch project-root/processes/generate_velocity/{generate_velocity_from_export_df.py,generate_velocity_from_velocity.py,README.md}
touch project-root/processes/validate_schema/{find_xsd_validation_step.py,README.md}
touch project-root/processes/export_task/{export_task.py,README.md}
touch project-root/site/app.py
touch project-root/examples/mzov/{mzov-1.0.0.xsd,mzov_example.xml}
touch project-root/examples/signatures/xmlsig_core.xsd
touch project-root/tests/test_generate_velocity.py
touch project-root/tests/test_validate_schema.py
touch project-root/shared/{utils.py,xsd_helpers.py,logger.py}
touch project-root/docs/{user_guide.docx,diagrams.drawio}
