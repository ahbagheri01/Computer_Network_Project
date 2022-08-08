
c=1
b=0
while [ $c > $b ]:
do
	echo "ping" | telnet 127.0.0.1 5002;
done

while $((1 > 0))
do
	echo "ping" | telnet 127.0.0.1 5002;
done

while [ 1 > 0 ];
do
	echo "ping" | telnet 127.0.0.1 5002;
done
