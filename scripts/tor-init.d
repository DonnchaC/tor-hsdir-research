#! /bin/sh

# $Id$
# $URL$

### BEGIN INIT INFO
# Provides:          tor
# Required-Start:    $local_fs $remote_fs $network $named $time
# Required-Stop:     $local_fs $remote_fs $network $named $time
# Should-Start:      $syslog
# Should-Stop:       $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Starts The Onion Router daemon processes
# Description:       Start The Onion Router, a TCP overlay
#                    network client that provides anonymous
#                    transport.

# Obtained from http://permalink.gmane.org/gmane.network.tor.relay/392
# Originally posted by Teun Nijssen (teun.nigseen@uvt.nl)

### END INIT INFO

set -e

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
NAME=tor
DESC='tor daemon'
DAEMON=/usr/sbin/tor
CONFIG=/etc/tor
USER=debian-tor
ARGS=""

NICE=""

test -x $DAEMON || exit 0
test -e $CONFIG || exit 0

mkdir -p -m 02700 /var/run/tor
chown debian-tor:debian-tor /var/run/tor

# Include tor defaults if available
if [ -f /etc/default/tor ]
then
        . /etc/default/tor
fi

command=$1
shift
instances=$*

instances() {
        case $instances in '')
                for c in $CONFIG/*.cfg
                do
                        base=${c##*/}
                        test -f "$c" && echo ${base%.cfg}
                done
        ;; *)
                echo "$instances"
        esac
}

start() {
        start-stop-daemon --start --quiet -oknodo --pidfile /var/run/tor/$1.pid --make-pidfile $NICE --exec $DAEMON -- -f $CONFIG/$1.cfg $ARGS
}

stop() {
        start-stop-daemon --stop --quiet --pidfile /var/run/tor/$1.pid --exec $DAEMON -- -f $CONFIG/$1.cfg $ARGS
}
reload() {
        start-stop-daemon --stop --signal 1 --quiet --pidfile /var/run/tor/$1.pid --exec $DAEMON -- -f $CONFIG/$1.cfg $ARGS
}

isrunning() {
        start-stop-daemon --stop --test --quiet --pidfile /var/run/tor/$1.pid --exec $DAEMON >/dev/null
}

case $command in
  start)
        if [ "$RUN_DAEMON" != "yes" ]; then
                echo "Not starting $DESC (Disabled in $DEFAULTSFILE)."
                exit 0
        fi

        echo -n "Starting $DESC:"

        if ulimit -n 65535; then
                echo "."
        else
                echo ": needed ulimit but FAILED."
                exit 0
        fi

        done=' (none)'
        for i in $(instances)
        do
                done=.
                start $i
                echo -n " $i"
        done
        echo $done
        ;;
  stop)
        echo -n "Stopping $DESC:"
        done=' (none)'
        for i in $(instances)
        do
                done=.
                stop $i
                echo -n " $i"
        done
        echo $done
        ;;
  reload|force-reload)
        # If the "reload" option is implemented, move the "force-reload"
        # option to the "reload" entry above. If not, "force-reload" is
        # just the same as "restart" except that it does nothing if the
        # daemon isn't already running.
        # check wether $DAEMON is running. If so, restart

        echo -n "(Force-)reloading $DESC:"
        done=' (none)'
        for i in $(instances)
        do
                if isrunning $i
                then
                        done=.
                        reload $i
                        echo -n " $i"
                        sleep 1
                fi
        done
        echo $done
        ;;
  restart)
    echo -n "Restarting $DESC:"
        done=' (none)'
        for i in $(instances)
        do
                done=.
                echo -n " $i"
                if isrunning $i
                then
                        stop $i
                        sleep 1
                fi
                start $i
        done
        echo $done
        ;;
  status)
        for i in $(instances)
        do
                if ! isrunning $i
                then
                        exit 1
                fi
        done
        exit 0
        ;;
  *)
        echo "Usage: $0 {start|stop|restart|force-reload|status}" >&2
        exit 1
        ;;
esac

exit 0
