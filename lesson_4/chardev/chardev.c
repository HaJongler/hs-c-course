#include <linux/kernel.h>
#include <linux/sched.h>
#include <linux/module.h>
#include <linux/fs.h>
#include <asm/uaccess.h> /* for put_user */

/*
 * Prototypes - this would normally go in a .h file
 */

int init_module(void);
void cleanup_module(void);
static int device_open(struct inode *, struct file *);
static int device_release(struct inode *, struct file *);
static ssize_t device_read(struct file *, char *, size_t, loff_t *);
static ssize_t device_write(struct file *, const char *, size_t, loff_t *);

#define SUCCESS 0
#define DEVICE_NAME "chardev"
#define BUF_LEN 1024
#define MAX_LINE_COUNT 128

/*
 * Global variables are declared as static, so are global within the file.
 */

static int eof_flag = 0;
static int Major;
static int device_counter = 0;
char *msg = NULL;
const char *read_message = "Hello, world !";



static struct file_operations fops = {
  .read = device_read,
  .write = device_write,
  .open = device_open,
  .release = device_release,
  .owner = THIS_MODULE
};

/*
 * This function is called when the module is loaded
 */
int init_module(void)
{
  Major = register_chrdev(0, DEVICE_NAME, &fops);

  if (Major < 0) {
    printk(KERN_ALERT "Registering char device failed with %d\n", Major);
    return Major;
  }

  printk(KERN_INFO "I was assigned major number %d. To talk to\n", Major);
  printk(KERN_INFO "the driver, create a dev file with\n");
  printk(KERN_INFO "'mknod /dev/%s c %d 0'.\n", DEVICE_NAME, Major);
  printk(KERN_INFO "Try various minor numbers. Try to cat and echo to\n");
  printk(KERN_INFO "the device file.\n");
  printk(KERN_INFO "Remove the device file and module when done.\n");

  return SUCCESS;
}

/*
 * This function is called when the module is unloaded
 */
void cleanup_module(void)
{
  /*
   * Unregister the device
   */
  unregister_chrdev(Major, DEVICE_NAME);
}

/*
 * Called when a process tries to open the device file, like
 * "cat /dev/mycharfile"
 */
static int device_open(struct inode *inode, struct file *filp)
{
  if (device_counter)
    return -EBUSY;

  device_counter++;

  try_module_get(THIS_MODULE);

  return SUCCESS;
}

/*
 * Called when a process closes the device file.
 */
static int device_release(struct inode *inode, struct file *filp)
{
  device_counter--;

  eof_flag = 0;
  module_put(THIS_MODULE);

  return SUCCESS;
}

/*
 * Called when a process, which already opened the dev file, attempts to read
 * from it.
 */
static ssize_t chardev_read(struct file *file, char *buf, size_t buf_len, 
		     loff_t *f_pos)
{
  unsigned long count = strlen(read_message) +1;
  int ret = 0;

  DPRINTK("want %lu chars starting a pos %lu\n",
	 (unsigned long)buf_len,(unsigned long)*f_pos);
  if (*f_pos >= count)
    goto end;			/* EOF */

  count -= *f_pos;

  if (buf_len < count)
    count = buf_len;

  DPRINTK("copying %lu chars starting a pos %lu\n",count,
	 (unsigned long)*f_pos);
  if (copy_to_user(buf,read_message + *f_pos, count )) {
    ret = -EFAULT;
    goto end;
  }
  ret = count;
  *f_pos += count;

 end:
  return ret;
}

/* 
 * This function is called when somebody tries to
 * write into our device file. 
 */
static ssize_t chardev_write(struct file *file, const char *buf, size_t buf_len, 
		      loff_t *f_pos)
{
  unsigned long count = MAX_LINE_COUNT;	/* Max write at a time */
  int ret = 0;
  char copy_buf[MAX_LINE_COUNT+1];
    
  DPRINTK("want %lu chars starting a pos %lu\n",
	 (unsigned long)buf_len,(unsigned long)*f_pos);
  
  if (buf_len < count)
    count = buf_len;

  if (copy_from_user(copy_buf,buf,count)) {
    ret = -EFAULT;
    goto end;
  }
  
  copy_buf[count] = '\0';
  ret = count;

  printk(KERN_INFO "writing:\n%s",copy_buf);
  
 end:
  return ret;
}