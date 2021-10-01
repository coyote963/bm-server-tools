import sys
import subprocess
import shlex

import fire
import asyncio

VOLUME_ROOT = ""
DESTINATION = ""
BMAN_LOCATION = ""

def copy_configuration(config_id: str):
    container_filename = f'{VOLUME_ROOT}/server_{container_id}.ini'
    copy_process = subprocess.run(['cp', container_filename, DESTINATION])
    if copy_process.status == 0:
        run_bman_server(container_id)
    else:
        sys.exit(copy_process.returncode)


def watchdog(process: asyncio.subprocess.Process):
    i = 0
    while i < 10:
        print(i)
        i += 1
    process.terminate()


async def run_bman_server(config_id: str):
    """Runs the BMAN server with the configuration file config_id"""
    cmd = 'sleep 100'
    #cmd = 'xvfb-run ./BoringManRewrite -dedicated_nogpu -noaudio -software -vanillaGFX'
    proc = await asyncio.create_subprocess_exec(
        'sleep','1000',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    watchdog(proc)
    stdout, stderr = await proc.communicate()


if __name__ == '__main__':
    fire.Fire({
        'copy': copy_configuration,
        'run': run_bman_server
    })