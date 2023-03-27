(defun gps-line ()
  " give output of the form 'Line X/Y'
    Y is total number of new line characters
    in buffer "
  (interactive)
  (let ( (cur (line-number-at-pos))
         (tot (how-many "\n" (point-min) (point-max))))

    (message "Line %s/%s" cur tot)))
