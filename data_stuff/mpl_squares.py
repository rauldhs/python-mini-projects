import matplotlib.pyplot as plt

x_values = range(1, 1001)
y_values = [x**2 for x in x_values]

plt.style.use('seaborn-v0_8-dark')
fig, ax = plt.subplots()

ax.scatter(x_values,y_values,s=10,c=y_values,cmap=plt.cm.bone)

ax.set_title("f(x) = x**2",fontsize=14)
ax.set_xlabel("x",fontsize=14)
ax.set_ylabel("f(x)",fontsize=14)

ax.tick_params(labelsize=14)

ax.axis([0,1100,0,1_100_100])
plt.show()