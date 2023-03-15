rule sftp_odm: 
    output: 
        SFTP_MATCH1_FILE 
	conda: 
        f'{ENVS_DIR}/pipeline.yaml' 
	params:
		ODATE=ODATE 
	group: 
       "pipeline" 
    script: 
       "../scripts/sftp_odm.py" 