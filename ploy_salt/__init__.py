import argparse
import os


class Shell(object):
    def __init__(self, instance):
        self.instance = instance

    def exec_cmd(self, cmd):
        chan = self.instance.conn.get_transport().open_session()
        rout = chan.makefile('rb', -1)
        rerr = chan.makefile_stderr('rb', -1)
        chan.exec_command(cmd)
        _out = rout.read()
        _err = rerr.read()
        _rc = chan.recv_exit_status()
        chan.close()
        return (_out, _err, _rc)

    def send(self, local, remote, makedirs=False):
        if makedirs:
            self.exec_cmd('mkdir -p {0}'.format(os.path.dirname(remote)))
        sftp = self.instance.paramiko.SFTPClient.from_transport(
            self.instance.conn.get_transport())
        sftp.put(local, remote)


class SaltCmd(object):
    """Run Salt"""

    def __init__(self, ctrl):
        self.ctrl = ctrl

    def __call__(self, argv, help):
        parser = argparse.ArgumentParser(
            prog="%s salt" % self.ctrl.progname,
            description=help,
        )
        instances = self.ctrl.get_instances(command='init_ssh_key')
        parser.add_argument("-r", "--raw", "--raw-shell",
                            dest="raw_shell", default=False,
                            action="store_true",
                            help="Don't execute a salt routine on the targets,"
                                 " execute a raw shell command")
        parser.add_argument("instance", nargs=1,
                            metavar="instance",
                            help="Name of the instance from the config.",
                            choices=list(instances))
        parser.add_argument("arguments", nargs='+',
                            metavar="arguments",
                            help="Arguments for salt.")
        args = parser.parse_args(argv)
        instance = instances[args.instance[0]]
        from salt.client.ssh import Single
        from salt.output import display_output
        from salt.utils import find_json
        salt_path = os.path.join(self.ctrl.config.path, 'salt')
        opts = dict(
            cython_enable=False,
            cachedir=os.path.join(salt_path, 'cache'),
            extension_modules=os.path.join(salt_path, 'extmods'),
            known_hosts_file=self.ctrl.known_hosts,
            raw_shell=args.raw_shell)
        single = Single(
            opts, args.arguments, instance.id,
            host=instance.get_host(), port=instance.get_port())
        single.shell = Shell(instance)
        (stdout, stderr, retcode) = single.run()
        ret = {
            'stdout': stdout,
            'stderr': stderr,
            'retcode': retcode,
        }
        try:
            data = find_json(stdout)
            if len(data) < 2 and 'local' in data:
                ret = data['local']
        except Exception:
            pass
        if not isinstance(ret, dict):
            p_data = {single.id: ret}
        elif 'return' not in ret:
            p_data = ret
        else:
            p_data = {single.id: ret.get('return', {})}
        display_output(p_data, 'nested', opts)


def get_commands(ctrl):
    return [
        ('salt', SaltCmd(ctrl))]


plugin = dict(
    get_commands=get_commands)
