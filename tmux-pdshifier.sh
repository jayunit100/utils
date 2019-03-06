#!/bin/bash
# A very useful and dumb tmux manager script for saved hosts

user=""

#### EDIT ABOVE THIS LINE

[ -f ./hosts ] && echo "Hosts file found: `cat hosts`" || echo "No 'hosts' file, make a pdsh hosts file and retry.'"

echo "Checks passed, starting tmux session for this cluster !"

#### Now create sessions

set -e
set -x

SESSION=${USER}-tmux-hosts-`pwd`
echo "Creating new tmux session"
tmux -2 new-session -d -s $SESSION

echo "created window"
curr_window=1

for i in `cat ./hosts` ; do
  if [[ $curr_window -gt 1 ]]; then
      tmux split-window -t $SESSION -v
  else
      tmux new-window -t $SESSION:1 -n '${curr_window}'
  fi
  tmux ls
  sleep 2
  num=$((curr_window - 1))
  tmux list-panes -t $SESSION
  tmux select-pane -t $SESSION:.$num
  tmux send-keys -t $SESSION:.$num "ssh-add ; ssh -v ${user}@${i}" C-m
  let "curr_window=curr_window+1"
done

echo "Created $curr_window windows for your massive cluster.  attaching now..."
sleep 1
tmux -2 attach -t $SESSION
